# -*- encoding: utf-8 -*-
from pyramid import testing
import sasha
import unittest


class ClusterTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_Instrument_01(self):
        instrument = sasha.newdomaintools.Instrument.objects.get(
            name='Alto Saxophone',
            )
        self.assertEqual(instrument.name, 'Alto Saxophone')
        self.assertEqual(instrument.transposition, 3)

    def test_get_link(self):
        instrument = sasha.newdomaintools.Instrument.objects.get(
            name='Alto Saxophone',
            )
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': instrument.dash_case_name,
                },
            )
        link = instrument.get_link(request)
        self.assertEqual(
            link.decode('utf-8'),
            '<a href="http://example.com/instruments/alto-saxophone/">Alto Saxophone</a>',
            )

    def test_get_url(self):
        instrument = sasha.newdomaintools.Instrument.objects.get(
            name='Alto Saxophone',
            )
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': instrument.dash_case_name,
                },
            )
        url = instrument.get_url(request)
        self.assertEqual(url, 'http://example.com/instruments/alto-saxophone/')

    def test_with_events(self):
        instruments = sasha.newdomaintools.Instrument.with_events()
        self.assertEqual(
            set(_.name for _ in instruments),
            set(['Alto Saxophone', 'Soprano Saxophone']),
            )

    def test_dash_case_name(self):
        instrument = sasha.newdomaintools.Instrument.objects.get(
            name='Alto Saxophone',
            )
        self.assertEqual(instrument.dash_case_name, 'alto-saxophone')

    def test_snake_case_name(self):
        instrument = sasha.newdomaintools.Instrument.objects.get(
            name='Alto Saxophone',
            )
        self.assertEqual(instrument.snake_case_name, 'alto_saxophone')