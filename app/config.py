from os import getenv

class Config(object):
  DEBUG = False

class ProductionConfig(Config):
  DATABASE_HOST = getenv('DATABASE_HOST', None)
  DATABASE_PORT = getenv('DATABASE_PORT', None)

class DevelopmentConfig(Config):
  DEBUG = True
  DATABASE_HOST = 'localhost'
  DATABASE_PORT = 27017
