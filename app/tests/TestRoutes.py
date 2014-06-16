import unittest
from datetime import timedelta
from app import myApp
from app import views


class TestRoutes(unittest.TestCase):

  def setUp(self):
    self.test_app = myApp.test_client()

  def test_root(self):
    rv = self.test_app.get('/', follow_redirects = True)
    assert "Welcome" in rv.data

  def test_getTimeDelta_defaultValue(self):
    chkDelta = views.getTimeDelta()
    assert(chkDelta == timedelta(days = 2 * 365)) # default 2 years

  def test_getTimeDelta_nonIntegerValue(self):
    chkDelta = views.getTimeDelta("2.25","years")
    assert(chkDelta == timedelta(days = int(2.25 * 365)))
