from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from sasha.tools import viewtools
import sasha
import unittest


class ViewTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_ClusterView_01(self):
        cluster = sasha.Cluster.objects.first()
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        view = viewtools.ClusterView(request)
        info = view()
        self.assertEqual(info['body_class'], 'clusters')
        self.assertEqual(
            info['title'],
            'SASHA | {} Cluster No.{}'.format(
                cluster.title_case_feature,
                cluster.cluster_id,
                ),
            )

    def test_EventView_01(self):
        event = sasha.Event.objects.first()
        md5 = event.md5
        instrument = event.fingering.instrument
        request = testing.DummyRequest(
            matchdict={
                'md5': event.md5,
                },
            )
        view = viewtools.EventView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(
            info['title'],
            'SASHA | {} Event: {}'.format(
                instrument.name,
                md5,
                ),
            )

    def test_FingeringView_01(self):
        event = sasha.Event.objects.first()
        instrument = event.fingering.instrument
        instrument_name = instrument.name.lower().replace(' ', '-')
        instrument_keys = ' '.join(event.fingering.key_names)
        fingering = event.fingering
        compact_representation = fingering.compact_representation
        request = testing.DummyRequest(
            matchdict={
                'compact_representation': compact_representation,
                'instrument_name': instrument_name,
                },
            )
        view = viewtools.FingeringView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['instrument_keys'], instrument_keys)
        self.assertEqual(info['instrument_name'], instrument.name)
        self.assertEqual(
            info['search_action'],
            'http://example.com/instruments/{}/{}/'.format(
                instrument_name,
                compact_representation,
                ),
            )
        self.assertEqual(
            info['title'],
            'SASHA | {} Fingering: {}'.format(
                instrument.name,
                instrument_keys
                ),
            )
        self.assertEqual(info['search_parameters']['with_pitch_classes'], set())
        self.assertEqual(info['search_parameters']['with_pitches'], set())
        self.assertEqual(info['search_parameters']['without_pitch_classes'], set())
        self.assertEqual(info['search_parameters']['without_pitches'], set())
        self.assertIsNotNone(info['paginator'])

    def test_HelpView_01(self):
        request = testing.DummyRequest()
        view = viewtools.HelpView(request)
        info = view()
        self.assertEqual(info['body_class'], 'help')
        self.assertEqual(info['title'], 'SASHA | Help')

    def test_HomeView_01(self):
        request = testing.DummyRequest()
        view = viewtools.HomeView(request)
        info = view()
        self.assertEqual(info['body_class'], 'home')
        self.assertEqual(info['title'], 'SASHA | Home')

    def test_InstrumentView_01(self):
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': 'alto-saxophone',
                },
            )
        view = viewtools.InstrumentView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Instrument: Alto Saxophone')

    def test_RandomEventView_01(self):
        request = testing.DummyRequest()
        view = viewtools.RandomEventView(request)
        info = view()
        self.assertEqual(type(info), HTTPFound)
        self.assertIn('/events/', info.location)

    def test_SearchView_01(self):
        request = testing.DummyRequest()
        view = viewtools.SearchView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Search')