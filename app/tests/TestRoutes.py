import unittest
from datetime import timedelta
from app import myApp
from app import views
import traceback, sys

class TestRoutes(unittest.TestCase):

  def setUp(self):
    self.test_app = myApp.test_client()

  def tearDown(self):
    del self.test_app

  def test_root(self):
    rv = self.test_app.get('/', follow_redirects = True)
    assert("Welcome" in rv.data)

  '''
  This test has caused me so many issues with Sniffer. It'll throw
  the assertion error correctly the first time, but the second time Sniffer
  runs it'll throw a 'Maximum-recursion level reached' error....

  def test_valid_stock(self):
    rv = self.test_app.get('/chart?ticker=TSLA', {})
    assert("TSLA" in rv.data)
  '''

  def test_getTimeDelta_defaultValue(self):
    chkDelta = views.getTimeDelta()
    assert(chkDelta == timedelta(days = 3 * 365)) # default 2 years

  def test_getTimeDelta_nonIntegerValue(self):
    chkDelta = views.getTimeDelta("2.25","years")
    assert(chkDelta == timedelta(days = int(2.25 * 365)))
