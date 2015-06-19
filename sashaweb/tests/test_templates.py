from webtest import TestApp
from sashaweb import main
import unittest


class TemplateTests(unittest.TestCase):

    def setUp(self):
        app = main({})
        self.testapp = TestApp(app)

    def test_404_01(self):
        path = '/bad-path/'
        response = self.testapp.get(path, status=404)
        self.assertIn(
            '<title>SASHA | 404 Not Found</title>',
            response,
            )

    def test_cluster_01(self):
        path = '/clusters/chroma/1/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Chroma Cluster No.1</title>',
            response,
            )

    def test_event_01(self):
        path = '/events/c5c19c1eb8b2fd2fa5d3e18566f10b3e/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Alto Saxophone Event: c5c19c1eb8b2fd2fa5d3e18566f10b3e</title>',
            response,
            )

    def test_fingering_01(self):
        path = '/instruments/alto-saxophone/1000000000000011100100000/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Alto Saxophone Fingering: 8va L1 L2 L3 R2</title>',
            response,
            )

    def test_instrument_01(self):
        path = '/instruments/alto-saxophone/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Instrument: Alto Saxophone</title>',
            response,
            )

    def test_help_01(self):
        path = '/help/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Help</title>',
            response,
            )

    def test_home_01(self):
        path = '/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Home</title>',
            response,
            )

    def test_random_01(self):
        path = '/random/'
        response = self.testapp.get(path, status=302)

    def test_search_01(self):
        path = '/search/'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Search</title>',
            response,
            )