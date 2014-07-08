from flask import Flask
from pymongo import MongoClient
from os import path, getenv
"""
calling it myApp to differentiate it from the package called app -- for my
benefit. I'm still learning.
"""
myApp = Flask(__name__, instance_relative_config = True)

#############  Load config files  #############################

if getenv('PRODUCTION_FLAG', None) is not None:
  myApp.config.from_object('app.config.ProductionConfig')
else:
  myApp.config.from_object('app.config.DevelopmentConfig')

###############################################################


# open up the DB connection
mongo = MongoClient(myApp.config['DATABASE_HOST'], myApp.config['DATABASE_PORT'])

from app import views # app refers to the package
