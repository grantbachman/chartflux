import pandas as pd

class Stock:
	'''
	This is the Stock object.
	'''

	def __init__(self, ticker):
		self.ticker=ticker.upper()
		
	def isNYSE(self):
		nyse = pd.read_csv('NYSE.txt', sep='\t')
		return nyse.apply(lambda x: self.ticker in x.values, axis=1).any()

	def isNASDAQ(self):
		nasdaq = pd.read_csv('NASDAQ.txt', sep='\t') 
		return nasdaq.apply(lambda x: self.ticker in x.values, axis=1).any()
