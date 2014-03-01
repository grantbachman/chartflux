import pandas as pd

class Stock:
	'''
	This is the Stock object.
	'''

	def __init__(self, ticker):
		self.ticker=ticker.upper()
		
	def is_NYSE(self):
		return self.is_ticker_in_file('NYSE.txt')

	def is_NASDAQ(self):
		return self.is_ticker_in_file('NASDAQ.txt')

	def is_ticker_in_file(self, filename):
		isFound = False
		f = open(filename, 'r')
		for line in f:
			pos = line.index('\t')	
			if line[0:pos] == self.ticker:
				isFound = True
		return isFound
