from pyramid import testing
from sasha.tools import viewtools
import sasha
import unittest


class HomeViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_HomeView_01(self):
        request = testing.DummyRequest()
        view = viewtools.HomeView(request)
        info = view()
        self.assertEqual(info['body_class'], 'home')
        self.assertEqual(info['title'], 'SASHA | Home')