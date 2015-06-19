from pyramid import testing
import unittest
from sashaweb import views


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('sashaweb')

    def tearDown(self):
        testing.tearDown()

    def test_HelpView(self):
        request = testing.DummyRequest()
        view = views.HelpView(request)
        info = view()
        self.assertEqual(info['body_class'], 'help')
        self.assertEqual(info['title'], 'SASHA | Help')

    def test_HomeView(self):
        request = testing.DummyRequest()
        view = views.HomeView(request)
        info = view()
        self.assertEqual(info['body_class'], 'home')
        self.assertEqual(info['title'], 'SASHA | Home')
