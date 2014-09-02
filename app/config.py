from os import getenv

class Config(object):
  DEBUG = False
  DATABASE_NAME = 'chartflux'

class ProductionConfig(Config):
  DATABASE_HOST = getenv('DATABASE_HOST', None)
  DATABASE_PORT = getenv('DATABASE_PORT', None)
  DATABASE_USER = getenv('DATABASE_USER', None)
  DATABASE_PASSWORD = getenv('DATABASE_PASSWORD', None)

class DevelopmentConfig(Config):
  DEBUG = True
  DATABASE_HOST = 'localhost'
  DATABASE_PORT = 5432
  DATABASE_USER = 'grant'
  DATABASE_PASSWORD = ''
