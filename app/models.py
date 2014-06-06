import datetime
from pandas import DataFrame
from pandas.io.data import DataReader


class Stock:
	'''
	This is the Stock object.

	Instance variables:
	ticker - Stock's ticker symbol
	start - The start date of the stock's data
	end - The end date of the stock's data
	data - The Pandas Dataframe containing the stock's data
	'''

	def __init__(self, ticker):
		self.ticker = ticker.upper()
		if self.get_data() is not None:
			self.is_valid = True
		else:
			self.is_valid = False

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
