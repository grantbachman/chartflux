import datetime
import pandas as pd
import numpy as np
from pandas.io.data import DataReader
import os
from app import myApp
import psycopg2, psycopg2.extras


class Stock(object):
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
		self.name, self.exchange = self.get_name_and_exchange() # pulled from file
		self.load_data() # load data from database
		if self.data is None:
			self.fetch_and_save_yahoo_data() # fetch and save to database
			self.load_data() # try to reload data from database

	def calc_sma(self, num_days, column_title=None):
		# Check that there are enough rows to be able to calculate a non-Nan value
		if self.data.shape[0] > num_days:
			column_title = 'sma' + str(num_days) if column_title is None else column_title
			self.data[column_title] = pd.rolling_mean(self.data['Adj Close'], num_days)

	def calc_ewma(self, num_days, column_title=None):
		# Check that there are enough rows to be able to calculate a non-Nan value
		if self.data.shape[0] > num_days:
			column_title = 'ewma' + str(num_days) if column_title is None else column_title
			self.data[column_title] = pd.ewma(self.data['Adj Close'], span=num_days)

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
		self.calc_ewma(50)
		self.calc_ewma(200)
		self.calc_rsi()
		self.calc_macd()
		#self.clear_NaN()
		#self.data = np.round(self.data,2)

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
		return (None,None)

	# gets run every night as part of a batch job
	def fetch_and_save_yahoo_data(self):
		connection = Connection()
		cur = connection.conn.cursor()
		query = """SELECT Date from ohlc
							 WHERE Stock = '%s'
							 ORDER BY Date DESC;""" % self.ticker
		cur.execute(query)
		row = cur.fetchone()
		try:
			# determine starting point from when to fetch data
			start_date = row[0] + datetime.timedelta(days=1)
		except:
			# no datapoints, just grab a bunch
			start_date = datetime.date(2000,1,1)
		try:
			data = DataReader(self.ticker, "yahoo", start_date, datetime.date.today())
			self._save_dataframe(connection, data)
		except:	   # stock data not retrieved
			pass
		connection.close()

	def load_data(self):
		connection = Connection()
		cur = connection.conn.cursor()
		query = """SELECT Date, Open, High, Low, Close, Volume, Adjusted_Close from ohlc
							 WHERE Stock = '%s'
							 ORDER BY Date ASC;""" % self.ticker
		cur.execute(query)
		rows = cur.fetchall()
		df = pd.DataFrame(columns = ('Date','Open','High','Low','Close','Volume','Adj Close'))
		df.set_index(keys='Date', drop=True, inplace=True)
		for row in rows:
			df.loc[row[0]] = [i[1] for i in enumerate(row) if i[0] > 0]
		connection.close()
		self.data = df if len(df) != 0 else None

	# Save the data just fetched from yahoo
	def _save_dataframe(self, connection, df):
		df2 = df.reset_index()
		cur = connection.conn.cursor()
		query = """INSERT INTO ohlc (Stock,Date,Open,High,Low,Close,Volume,Adjusted_Close)
													VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
		for row in df2.values:
			row[0] = row[0].date()
			row = np.insert(row, 0, self.ticker)
			cur.execute(query, tuple(row))
			connection.conn.commit()

	def _create_ohlc_table():
		connection = Connection()
		cur = connection.conn.cursor()
		query = """CREATE TABLE IF NOT EXISTS ohlc(
			id bigserial primary key,
			Stock varchar(6) NOT NULL,
			Date date NOT NULL,
			Open decimal(10,2) NOT NULL,
			High decimal(10,2) NOT NULL,
			Low decimal(10,2) NOT NULL,
			Close decimal(10,2) NOT NULL,
			Volume integer NOT NULL,
			Adjusted_Close decimal(10,2) NOT NULL
			);"""
		try:
			print('Trying to crate ohlc table')
			curr.execute(query)
		except:
			print('Failed trying to create ohlc table')
		connection.close()

##########################

class Connection(object):
	def __init__(self):
		try:
			self.conn = psycopg2.connect("dbname='" + str(myApp.config['DATABASE_NAME']) + "'" +
															"host='" + str(myApp.config['DATABASE_HOST']) + "'" +
															"user='" + str(myApp.config['DATABASE_USER']) + "'" +
															"password='" + str(myApp.config['DATABASE_PASSWORD']) + "'" +
															"port='" + str(myApp.config['DATABASE_PORT']) + "'"
															)
			print("Connection established.")
		except:
			self.conn = None
			print("Connection refused.")

	def close(self):
		if self.conn is not None:
				self.conn.close()
				print("Connection closed.")
