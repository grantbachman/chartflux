#!../env/bin/python
import sys, os
from types import NoneType
import datetime as dt
from pandas import Timestamp, DataFrame, Series
from pandas.util.testing import assert_frame_equal
import pandas as pd
import pickle
from models import Stock
import unittest

class TestStock(unittest.TestCase):

	def setUp(self):
		self.stock = Stock("tsla")

	def test_init(self):
		self.failIf(self.stock.ticker != "TSLA")

	def test_set_data(self):
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		self.stock.set_data(start, end)
		self.failUnless(isinstance(self.stock.start, dt.date))
		self.failUnless(isinstance(self.stock.end, dt.date))
		self.failUnless(isinstance(self.stock.data, DataFrame))

	#	Don't test these all the time. It actually calls out to Yahoo and
	#	says "Hello? I would like some stock data, please."

	def validate_test_data(self):
		start = dt.date(2014, 02, 24)
		end = dt.date(2014, 02, 28)
		data_from_yahoo = self.stock.get_data(start, end)
		tsla_file = open('tsla_1week_20140224_20140228.pkl', 'r')
		up = pickle.Unpickler(tsla_file)
		data_from_file = up.load()
		self.failUnless(assert_frame_equal(data_from_file,data_from_yahoo) is None)

	# Should return a valid DataFrame
	def test_valid_stock(self):
		stock = Stock("TSLA")
		end = dt.date.today()
		start = end - dt.timedelta(days = 7)
		data = stock.get_data(start, end)
		self.failIf(data is None)
		self.failUnless(isinstance(data, DataFrame))

	# Should NOT return a valid DataFrame
	def test_invalid_stock(self):
		stock = Stock("asdfasf7")
		end = dt.date.today()
		start = end - dt.timedelta(days = 7)
		data = stock.get_data(start, end)
		self.failIf(data is not None)
		self.failUnless(type(data) is NoneType)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
