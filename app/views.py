import sys, os
import datetime
from app import myApp
from models import Stock
from forms import TickerForm
from flask import render_template, url_for, redirect, request 

@myApp.route('/')
def root():    # flask doesn't very much like including self as param 1
	return redirect(url_for('index'))

@myApp.route('/index')
def index():
	form = TickerForm()
	return render_template('index.html', form = form)

@myApp.route('/chart/<ticker>', methods = ['GET'])
def chart(ticker):
	stock = Stock(ticker)
	# find the dates for today and 3 years ago
	default_end = datetime.date.today()
	default_start = default_end - datetime.timedelta(days=3*365)   
	data = stock.get_data(default_start, default_end)
