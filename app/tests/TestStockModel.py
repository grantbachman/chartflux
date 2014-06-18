#!../env/bin/python
import sys, os
from types import NoneType
import datetime as dt
from pandas import Timestamp, DataFrame, Series
from pandas.util.testing import assert_frame_equal
import pickle
from app import myApp
from app.models import Stock
import unittest

class TestStockModel(unittest.TestCase):

	def test_init_succeed(self):
		self.stock = Stock("tsla")
		self.failIf(self.stock.ticker != "TSLA")
		self.failIf(self.stock.is_valid is not True)
		self.failUnless(self.stock.is_valid is True)

	def test_init_fail(self):
		self.stock = Stock("adsfadf")
		assert(self.stock.is_valid is False)

	def test_get_name_and_exchange_is_success(self):
		self.stock = Stock("GOOG")
		return_tuple = self.stock.get_name_and_exchange()
		assert(return_tuple[0] == "Google Inc.")
		print return_tuple
		assert(return_tuple[1] == "NASDAQ")

	def test_get_name_and_exchange_is_failure(self):
		self.stock = Stock("afdasdf")
		return_tuple = self.stock.get_name_and_exchange()
		assert(return_tuple is None)


	def test_set_data(self):
		self.stock = Stock("tsla")
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		self.stock.set_data(start, end)
		self.failUnless(isinstance(self.stock.start, dt.date))
		self.failUnless(isinstance(self.stock.end, dt.date))
		self.failUnless(isinstance(self.stock.data, DataFrame))

	# This function throws an error when not run from inside the app/ directory...
	# need to figure that one out...
	def validate_test_data(self):
		self.stock = Stock("tsla")
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		data_from_yahoo = self.stock.get_data(start, end)
		tsla_file = open(os.path.join(myApp.root_path,'tests/tsla_1week_20140224_20140228.pkl'), 'r')
		up = pickle.Unpickler(tsla_file)
		data_from_file = up.load()
		assert_frame_equal(data_from_file, data_from_yahoo)

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
