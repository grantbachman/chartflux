import datetime
from pandas import DataFrame
from pandas.io.data import DataReader
from app import myApp
import os


class Stock:
	'''
	This is the Stock object.

	Instance variables:
	ticker - Stock's ticker symbol
	name - Name of the company
	exchange - Exchange on which the stock is listed.
	start - The start date of the stock's data
	end - The end date of the stock's data
	data - The Pandas Dataframe containing the stock's data
	'''

	def __init__(self, ticker):
		self.ticker = ticker.upper()
		name_exchange_tuple = self.get_name_and_exchange()
		if name_exchange_tuple is not None:
			self.name, self.exchange = name_exchange_tuple
			self.is_valid = True
		else:
			self.is_valid = False

	def get_name_and_exchange(self):
		symbol_file_path = os.path.join(myApp.root_path,'static/symbols.txt')
		with open(symbol_file_path, 'r') as inFile:
				for line in inFile:
					split = line.strip('\n').split('\t')
					if split[1] == self.ticker:
						return (split[2], split[0])
		return None


	# Set's a stock's data without returning anything
	def set_data(self, start=datetime.date.today() - datetime.timedelta(days=1),
										 end=datetime.date.today()):
		self.start = start
		self.end = end
		self.data = self.get_data(start, end)

	# return either the stock data or None
	# if nothing is passed, it just grabs yesterday's data
	def get_data(self, start=datetime.date.today() - datetime.timedelta(days=1),
										 end=datetime.date.today()):
		try:
			data = DataReader(self.ticker, "yahoo", start, end)
		except:	   # stock data not retrieved
			data = None
		if isinstance(data, DataFrame):
			return data
		else:
			self.data, self.start, self.end = None, None, None
			return None
