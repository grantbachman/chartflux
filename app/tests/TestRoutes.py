import unittest
from app import myApp


class TestRoutes(unittest.TestCase):

  def setUp(self):
    self.test_app = myApp.test_client()

  def test_root(self):
    rv = self.test_app.get('/', follow_redirects = True)
    assert "Welcome" in rv.data
