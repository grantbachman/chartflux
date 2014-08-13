#!../env/bin/python
import sys, os
import datetime
from types import NoneType
import datetime as dt
import pandas as pd
from pandas import Timestamp, DataFrame, Series
from app import myApp
from app.models import Stock
from mock import Mock, MagicMock, patch
from unittest import TestCase
import aapl_test_data

class TestStockModel(TestCase):

	def setUp(self):
		self.stock = MagicMock(Stock)
		self.stock.ticker = "AAPL"
		self.stock.data = DataFrame(aapl_test_data.data)
		self.stock.data.index.name = 'Date' # can't set the name w/ pd.DataFrame
		self.stock.name = 'Apple Inc.'
		self.stock.exchange = 'NASDAQ'

	def test_init(self):
		assert(self.stock.data is not None)

	@patch('app.models.pd.rolling_mean', return_value=Series())
	def test_calc_sma(self, patched_rolling_mean):
		# for some reason, the test doesn't pass when I directly pass in
		# self.stock.data['Adj Close'] to the assert_called_with function. It
		# bombs out somewhere deep in Pandas... I'll need to figure that out later
		adj_close = self.stock.data['Adj Close']
		Stock.calc_sma(self.stock, 3)
		patched_rolling_mean.assert_called_with(adj_close, 3)
		assert(isinstance(self.stock.data['sma3'], Series) is not None)

	def test_get_name_and_exchange(self):
		name_exchange_tuple = Stock.get_name_and_exchange(self.stock)
		assert(name_exchange_tuple[0] == 'Apple Inc.')
		assert(name_exchange_tuple[1] == 'NASDAQ')

	@patch('app.models.DataReader')
	def test_set_data(self, patched_DataReader):
		num_days = 2 * 365
		Stock.set_data(self.stock, num_days)
		end = datetime.date.today()
		start = end - datetime.timedelta(days = num_days + 365)
		patched_DataReader.assert_called_with('AAPL', 'yahoo', start, end)

	# Tests Stock.clear_NaN
	def test_NaN(self):
		Stock.calc_sma(self.stock,3)
		# After calculating an average, ensure their are NaNs in the right places
		assert(pd.isnull(self.stock.data.iloc[0]['sma3']))
		assert(not pd.isnull(self.stock.data.iloc[2]['sma3']))
		shape_before_clearing = self.stock.data.shape # tuple of (rows, columns)
		Stock.clear_NaN(self.stock)
		# assert the number of rows decreases by 2
		assert(self.stock.data.shape[0] == shape_before_clearing[0] - 2)
		# assert the number of columns remains the same
		assert(self.stock.data.shape[1] == shape_before_clearing[1])
		# Ensure there are no more NaNs.
		assert(not pd.isnull(self.stock.data.iloc[0]['sma3']))


def main():
	unittest.main()

if __name__ == '__main__':
	main()
