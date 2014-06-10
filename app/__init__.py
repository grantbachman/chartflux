from flask import Flask
"""
calling it myApp to differentiate it from the package called app -- for my
benefit. I'm still learning.
"""
myApp = Flask(__name__, instance_relative_config = True)

myApp.config.from_object('app.config')
myApp.config.from_pyfile('config.py')
from app import views # app refers to the package
