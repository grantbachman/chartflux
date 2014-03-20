from flask import Flask
import config

myApp = Flask(__name__)
myApp.config.from_object(config)

from app import views
