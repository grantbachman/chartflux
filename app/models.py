import datetime
import pandas as pd
import numpy as np
from pandas.io.data import DataReader
import os

class Stock:
	'''
	This is the Stock object.

	Instance variables:
	ticker - Stock's ticker symbol
	name - Name of the company
	exchange - Exchange on which the stock is listed.
	data - The Pandas DataFrame containing the stock's data
	'''

	def __init__(self, ticker):
		self.ticker = ticker.upper()
		self.name, self.exchange = self.get_name_and_exchange()
		self.set_data(2*365)

	def calc_sma(self, num_days, column_title=None):
		# Check that there are enough rows to be able to calculate a non-Nan value
		if self.data.shape[0] > num_days:
			column_title = 'sma' + str(num_days) if column_title is None else column_title
			self.data[column_title] = pd.rolling_mean(self.data['Adj Close'], num_days)

	def calc_rsi(self):
		x = self.data['Adj Close'].copy() # deep copy the data into a series
		delta = x.diff().dropna()
		rsiDF = pd.DataFrame({"Up" : delta, "Down" : delta})
		rsiDF['Up'] = rsiDF['Up'][rsiDF['Up'] > 0]
		rsiDF['Down'] = rsiDF['Down'][rsiDF['Down'] < 0]
		rsiDF = rsiDF.fillna(value=0)
		rsiDF['UpMean'] = pd.rolling_mean(rsiDF['Up'],14)
		rsiDF['DownMean'] = pd.rolling_mean(rsiDF['Down'],14).abs()
		rsiDF['RS'] = rsiDF['UpMean'] / rsiDF['DownMean']
		rsiDF['RSI'] = 100 - (100/(1+rsiDF['RS']))
		self.data['RSI'] = rsiDF['RSI']

	def calc_macd(self):
		macdDF = pd.DataFrame({ 'Adj Close' : self.data['Adj Close'].copy() })
		macdDF['EMA12'] = pd.ewma(macdDF['Adj Close'], span=12)
		macdDF['EMA26'] = pd.ewma(macdDF['Adj Close'], span=26)
		macdDF['MACD'] = macdDF['EMA12'] - macdDF['EMA26']
		macdDF['Signal'] = pd.ewma(macdDF['MACD'],span=9)
		self.data['MACD'] = macdDF['MACD']
		self.data['MACD-Signal'] = macdDF['Signal']

	def calc_all(self):
		self.calc_sma(50)
		self.calc_sma(200)
		self.calc_rsi()
		self.calc_macd()
		self.clear_NaN()
		self.data = np.round(self.data,2)

	# Clear away any rows that are blank as a result of calculating averages
	# E.G. the first two rows will be blank when calculating the 3-day SMA
	def clear_NaN(self):
		self.data.dropna(0,'any',None,None,True)

	def get_name_and_exchange(self):
		symbol_file_path = os.path.join(os.path.dirname(__file__),'static/symbols.txt')
		with open(symbol_file_path, 'r') as inFile:
				for line in inFile:
					split = line.strip('\n').split('\t')
					if split[1] == self.ticker:
						return (split[2], split[0]) # split[2] = name, split[0] = exchange
		return None

	def set_data(self,num_days):
		lookback_days = num_days + 365 # calculating 200 day moving average
		end = datetime.date.today()
		start = end - datetime.timedelta(days = lookback_days)
		try:
			self.data = DataReader(self.ticker, "yahoo", start, end)
		except:	   # stock data not retrieved
			self.data = None
