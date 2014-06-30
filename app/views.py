import sys, os
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
    stock.calc_all()
    format_data = stock.data.reset_index()  # DateTimeIndex to column
    format_data = format_data.to_json(date_format='epoch', orient='records')
    # Markup tells jinja2 that the object is safe for rendering, without
    # escaping the quotes (caused problems when creating JSON object).
    format_data = Markup(format_data)
    # need to redirect instead
    return render_template('chart.html', stock=stock, data=format_data)

def getTimeDelta(value=3, unit="years"):
  try:
    value = float(value)
  except:
    value = 3
  if unit == "days":
    return dt.timedelta(days = int(value))
  elif unit == "weeks":
    return dt.timedelta(weeks = int(value))
  elif unit == "months":
    return dt.timedelta(days = int(value * 30))
  else:
    return dt.timedelta(days = int(value * 365))
