import sys, os
import datetime as dt
from app import myApp
from models import Stock
from forms import TickerForm
from jinja2 import Markup
from flask.ext.wtf import Form
from flask import render_template, url_for, redirect, request, flash,\
                  session, abort

@myApp.route('/')
def root():
  return redirect(url_for('index'))

@myApp.route('/index', methods = ['GET', 'POST'])
def index():
  form = TickerForm()
  if request.method == 'POST':
    if form.validate == False:
      flash('Enter a valid stock symbol')
      return render_template('index.html',form=form)
    else:
      ticker = request.form['ticker']
      stock = Stock(ticker)
      end = dt.date.today()
      start = end - dt.timedelta(days = 5)
      stock.set_data(start, end)
      # Markup tells jinja2 that the object is safe for rendering, without
      # escaping the quotes (caused problems when creating JSON object).
      data = Markup(stock.data.to_json(date_format='iso', orient='index'))
      # need to redirect instead
      return render_template('chart.html', stock=stock, data=data)
  elif request.method == 'GET':
      return render_template('index.html',form=form)

@myApp.before_request
def csrf_protect():
	if request.method == 'POST':
		token = session.pop('_csrf_token', None)
		if not token or token != request.form.get('_csrf_token'):
			abort(403)


def generate_csrf_token():
	if '_csrf_token' not in session:
		session['_csrf_token'] = os.urandom(24).encode('hex')
	return session['_csrf_token']

myApp.jinja_env.globals['csrf_token'] = generate_csrf_token
