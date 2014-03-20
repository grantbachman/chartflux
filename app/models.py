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


	# return either the stock data or 0
	def fetch_data(self, start, end): 
		try:
			data = DataReader(self.ticker, "yahoo", start, end)
		except:	   # stock data not retrieved		
			data = None 
		if isinstance(data, DataFrame):
			return data
		else:
			self.data, self.start, self.end = None, None, None
			return None 
