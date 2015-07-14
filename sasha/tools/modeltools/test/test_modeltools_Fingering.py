# -*- encoding: utf-8 -*-
from pyramid import testing
import sasha
import unittest


class FingeringTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_Fingering_01(self):
        event = sasha.modeltools.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        fingering = event.fingering
        self.assertEqual(fingering.instrument.name, 'Alto Saxophone')
        self.assertEqual(fingering.compact_representation, '0010000000001010001110000')

    def test_find_similar_fingerings(self):
        event = sasha.modeltools.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        fingering = event.fingering
        similar_fingerings = fingering.find_similar_fingerings()
        self.assertEqual(len(similar_fingerings), 4)

    def test_get_url(self):
        event = sasha.modeltools.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        fingering = event.fingering
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': fingering.instrument.name,
                'compact_representation': fingering.compact_representation,
                },
            )
        url = fingering.get_url(request)
        self.assertEqual(
            url,
            'http://example.com/instruments/alto-saxophone/0010000000001010001110000/',
            )

    def test_get_link(self):
        event = sasha.modeltools.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        fingering = event.fingering
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': fingering.instrument.name,
                'compact_representation': fingering.compact_representation,
                },
            )
        link = fingering.get_link(request)
        self.assertEqual(
            link.encode('utf-8'),
            '<a href="http://example.com/instruments/alto-saxophone/0010000000001010001110000/">Bf Ef L1 R1 R2 R3</a>',
            )

    def test_name(self):
        event = sasha.modeltools.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        fingering = event.fingering
        self.assertEqual(
            fingering.name,
            'Bf Ef L1 R1 R2 R3',
            )