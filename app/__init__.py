from flask import Flask
import os
myApp = Flask(__name__)

myApp.config['CSRF_ENABLED'] = True
myApp.config['SECRET_KEY'] = os.urandom(24)

from app import views
