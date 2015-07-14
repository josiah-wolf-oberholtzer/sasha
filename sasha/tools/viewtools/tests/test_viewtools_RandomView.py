from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from sasha.tools import viewtools
import sasha
import unittest


class RandomViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_RandomEventView_01(self):
        request = testing.DummyRequest()
        view = viewtools.RandomEventView(request)
        info = view()
        self.assertEqual(type(info), HTTPFound)
        self.assertIn('/events/', info.location)
