from flask import Flask
from pymongo import MongoClient
import os.path
"""
calling it myApp to differentiate it from the package called app -- for my
benefit. I'm still learning.
"""
myApp = Flask(__name__, instance_relative_config = True)

#############  Load config files  #############################
# loads the default configuration in chartflux/app/config.py
myApp.config.from_object('app.config')

# override app.config with chartflux/instance/config.py if it exists
if os.path.isfile(os.path.join(myApp.instance_path,'config.py')):
  myApp.config.from_pyfile('config.py')
###############################################################

# open up the DB connection
mongo = MongoClient(myApp.config['MONGO_DBNAME'], myApp.config['MONGO_PORTNUM'])

from app import views # app refers to the package
