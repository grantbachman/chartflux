import datetime
from pandas import DataFrame, rolling_mean
from pandas.io.data import DataReader
#from app import myApp
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
	show_from - the starting date to show the data.
	- Why this is needed: in order to display a stock's moving average, there
				there would be no moving average value until the number of days for
				which the average is comprised is met. e.g. 200 day moving average needs
				200 days worth of prior data to have a non-zero value.
	'''

	def __init__(self, ticker):
		self.ticker = ticker.upper()
		name_exchange_tuple = self.get_name_and_exchange()
		if name_exchange_tuple is not None:
			self.name, self.exchange = name_exchange_tuple
			self.is_valid = True
		else:
			self.is_valid = False

	def calc_sma_20(self):
		self.data['sma20'] = rolling_mean(self.data['Adj Close'], 20)

	def calc_sma_50(self):
		self.data['sma50'] = rolling_mean(self.data['Adj Close'], 50)

	def calc_sma_200(self):
		self.data['sma200'] = rolling_mean(self.data['Adj Close'], 200)

	def get_name_and_exchange(self):
		# need to figure out how to get the root path of the app without importing
		# it, because this won't work on other machines, obviously.
		symbol_file_path = '/Users/grant/Code/python/chartflux/app/static/symbols.txt'
		with open(symbol_file_path, 'r') as inFile:
				for line in inFile:
					split = line.strip('\n').split('\t')
					if split[1] == self.ticker:
						return (split[2], split[0])
		return None

	def set_data(self):
		display_days = 2 * 365	# 2 years
		lookback_days = display_days + 365 # calculating 200 day moving average
		self.end = datetime.date.today()
		self.start = self.end - datetime.timedelta(days = lookback_days)
		self.display_start_date = self.end - datetime.timedelta(days = display_days)
		try:
			data = DataReader(self.ticker, "yahoo", self.start, self.end)
		except:	   # stock data not retrieved
			data = None
		if isinstance(data, DataFrame):
			self.data = data
			self.is_valid = True
		else:
			self.is_valid = False
