import datetime
from pandas import DataFrame, rolling_mean
from pandas.io.data import DataReader
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
			self.set_data()
		else:
			self.is_valid = False
			self.data = None

	def calc_sma(self, num_days, column_title=None):
		# Check that there are enough rows to be able to calculate a non-Nan value
		if self.data.shape[0] > num_days:
				column_title = 'sma' + str(num_days) if column_title is None else column_title
				self.data[column_title] = rolling_mean(self.data['Adj Close'], num_days)

		# Check that there are enough rows to be able to calculate a non-Nan value
		if self.data.shape[0] > 50:
			self.data['sma50'] = rolling_mean(self.data['Adj Close'], 50)

	def calc_all(self):
		self.calc_sma(20)
		self.calc_sma(50)
		self.calc_sma(200)
		self.clear_NaN()

	def clear_NaN(self):
		self.data.dropna(0,'any',None,None,True)

	def get_name_and_exchange(self):
		symbol_file_path = os.path.join(os.path.dirname(__file__),'static/symbols.txt')
		with open(symbol_file_path, 'r') as inFile:
				for line in inFile:
					split = line.strip('\n').split('\t')
					if split[1] == self.ticker:
						return (split[2], split[0])
		return None

	def set_data(self):
		display_days = 3 * 365
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
