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
		self.stock.set_data()
		self.failUnless(isinstance(self.stock.data, DataFrame))

	# Should return a valid DataFrame
	def test_valid_stock(self):
		stock = Stock("TSLA")
		stock.set_data()
		self.failIf(stock.data is None)
		self.failUnless(isinstance(stock.data, DataFrame))
		self.failIf(stock.is_valid is not True)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
