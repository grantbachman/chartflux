import sys, os
import re
import datetime as dt
from app import myApp
from models import Stock
from jinja2 import Markup
from flask import render_template, url_for, redirect, request, flash,\
                  session, abort

@myApp.route('/')
@myApp.route('/index')
def index():
  return render_template('index.html')

@myApp.route('/d3')
def d3():
  return render_template('d3.html')


@myApp.route('/chart')
def show_stock():
  stock = request.args.get('ticker')
  value = request.args.get('value')
  unit = request.args.get('unit')
  stock = Stock(stock)
  if not stock.is_valid:
    error = "Invalid ticker symbol."
    return render_template('index.html', error = error)
  else:
    end = dt.date.today()
    td = getTimeDelta(value,unit)
    start = end - td
    stock.set_data(start, end)
    format_data = stock.data.reset_index()  # DateTimeIndex to column
    format_data = format_data.to_json(date_format='iso', orient='records')

    # Markup tells jinja2 that the object is safe for rendering, without
    # escaping the quotes (caused problems when creating JSON object).
    format_data = Markup(format_data)
    # need to redirect instead
    return render_template('chart.html', stock=stock, data=format_data)

def getTimeDelta(value=1, unit="years"):
  try:
    value = int(value)
  except:
    value = 1
  if unit == "days":
    return dt.timedelta(days = value)
  elif unit == "weeks":
    return dt.timedelta(weeks = value)
  elif unit == "months":
    return dt.timedelta(days = (value * 30))
  else:
    return dt.timedelta(days = (value * 365))



@myApp.route('/stock/verify', methods = ['POST'])
def verify_stock():
  ticker = request.form['ticker']
  if ticker == "":
    return redirect(url_for('index'))
  return redirect(url_for('show_stock', ticker=ticker))
