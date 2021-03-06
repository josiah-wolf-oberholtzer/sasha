from sasha import main
from webtest import TestApp
import os
import sasha
import unittest


class TemplateTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
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

    def test_cluster_02(self):
        path = '/clusters/mfcc/3/?instrument=alto_saxophone'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | MFCC Cluster No.3</title>',
            response,
            )


    def test_event_01(self):
        event = sasha.Event.objects.first()
        instrument = event.fingering.instrument
        md5 = event.md5
        path = '/events/{}/'.format(md5)
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | {} Event: {}</title>'.format(
                instrument.name,
                md5,
                ),
            response,
            )

    def test_fingering_01(self):
        event = sasha.Event.objects.first()
        fingering = event.fingering
        instrument_name = fingering.instrument.name
        instrument_dashcase_name = instrument_name.lower().replace(' ', '-')
        compact_representation = fingering.compact_representation
        instrument_keys = ' '.join(fingering.key_names)
        path = '/instruments/{}/{}/'.format(
            instrument_dashcase_name,
            compact_representation,
            )
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | {} Fingering: {}</title>'.format(
                instrument_name,
                instrument_keys,
                ),
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

    def test_search_02(self):
        path = '/search/?with_pitches=d4&without_pitches=d4'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Search</title>',
            response,
            )

    def test_search_03(self):
        path = '/search/?with_pitch_classes=d&without_pitch_classes=d'
        response = self.testapp.get(path, status=200)
        self.assertIn(
            '<title>SASHA | Search</title>',
            response,
            )