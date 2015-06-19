from pyramid import testing
import unittest
from sashaweb.views import HomeView


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('sashaweb')

    def tearDown(self):
        testing.tearDown()

    def test_HomeView_01(self):
        request = testing.DummyRequest()
        view = HomeView(request)
        info = view()
        self.assertEqual(info['body_class'], 'home')
        self.assertEqual(info['title'], 'SASHA | Home')