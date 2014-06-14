#!../env/bin/python
import sys, os
from types import NoneType
import datetime as dt
from pandas import Timestamp, DataFrame, Series
from pandas.util.testing import assert_frame_equal
import pandas as pd
import pickle
from app.models import Stock
import unittest

class TestStockModel(unittest.TestCase):

	def test_init(self):
		self.stock = Stock("tsla")
		self.failIf(self.stock.ticker != "TSLA")
		self.failIf(self.stock.is_valid is not True)
		self.failUnless(self.stock.is_valid is True)

	def test_set_data(self):
		self.stock = Stock("tsla")
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		self.stock.set_data(start, end)
		self.failUnless(isinstance(self.stock.start, dt.date))
		self.failUnless(isinstance(self.stock.end, dt.date))
		self.failUnless(isinstance(self.stock.data, DataFrame))

	#	Don't test these all the time. It actually calls out to Yahoo and
	#	says "Hello? I would like some stock data, please."

	def validate_test_data(self):
		self.stock = Stock("tsla")
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		data_from_yahoo = self.stock.get_data(start, end)
		print os.getcwd()
		tsla_file = open('tests/tsla_1week_20140224_20140228.pkl', 'r')
		up = pickle.Unpickler(tsla_file)
		data_from_file = up.load()
		self.failUnless(assert_frame_equal(data_from_file,data_from_yahoo) is None)

	# Should return a valid DataFrame
	def test_valid_stock(self):
		stock = Stock("TSLA")
		stock.set_data()
		self.failIf(stock.data is None)
		self.failUnless(isinstance(stock.data, DataFrame))
		self.failIf(stock.is_valid is not True)

	# Should NOT return a valid DataFrame
	def test_invalid_stock(self):
		stock = Stock("asdfasf7")
		stock.set_data()
		self.failIf(stock.data is not None)
		self.failUnless(type(stock.data) is NoneType)
		self.failIf(stock.is_valid is True)

def main():
	unittest.main()

if __name__ == '__main__':
	main()