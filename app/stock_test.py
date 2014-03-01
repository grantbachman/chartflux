from  stock import *
import unittest

class StockTest(unittest.TestCase):

	def test_should_be_nyse(self):
		stock = Stock("aa")  # Alcoa
		self.failIf(not stock.is_NYSE())

	def test_should_not_be_nyse(self):
		stock = Stock("xxxxxx")
		self.failIf(stock.is_NYSE()) 

	def test_should_be_nasdaq(self):
		stock = Stock("aapl")  # Apple
		self.failIf(not stock.is_NASDAQ())

	def test_should_not_be_nasdaq(self):
		stock = Stock("xxxxxx")
		self.failIf(stock.is_NASDAQ()) 



def main():
	unittest.main()

if __name__ == '__main__':
	main()


