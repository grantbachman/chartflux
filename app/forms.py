from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class TickerForm(Form):
	ticker = TextField('Ticker', validators = [ DataRequired() ])