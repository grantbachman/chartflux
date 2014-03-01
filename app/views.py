from app import myApp
from flask import render_template, url_for, redirect

@myApp.route('/')
def root():
	return redirect(url_for('index'))

@myApp.route('/index')
def index():
	return render_template('index.html')

@myApp.route('/chart/<ticker>')
def chart(ticker):
	ticker = ticker.upper()
	return render_template('index.html', ticker=ticker)
