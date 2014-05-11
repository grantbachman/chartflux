from wtforms import Form, TextField
from wtforms import validators

class TickerForm(Form):
	ticker = TextField('Ticker', validators=[validators.Length(max=6),
																validators.DataRequired()])
