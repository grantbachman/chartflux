from flask import Flask, g
import psycopg2
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

def connect_db():
  # open up the DB connection
  try:
    conn = psycopg2.connect("dbname='" + str(myApp.config['DATABASE_NAME']) + "'" +
                            "host='" + str(myApp.config['DATABASE_HOST']) + "'" +
                            "user='" + str(myApp.config['DATABASE_USER']) + "'" +
                            "password='" + str(myApp.config['DATABASE_PASSWORD']) + "'" +
                            "port='" + str(myApp.config['DATABASE_PORT']) + "'"
                            )
    return conn
  except:
    print("Unable to establish database connection.")

@myApp.before_request
def before_request():
  pass
  #g.db_conn=connect_db()

@myApp.teardown_request
def teardown_request(exception):
  pass
  #if g.db_conn is not None:
  #  g.db_conn.close()

from app import views # app refers to the package
