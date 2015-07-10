from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from sasha import views
import os
import sasha
import unittest


class ViewTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    @unittest.skipIf(
        os.environ.get('TRAVIS') == 'true',
        "Clustering is broken under Travis-CI."
        )
    def test_ClusterView_01(self):
        cluster = sasha.Cluster.get_one(id=1)
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        view = views.ClusterView(request)
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
        event = sasha.Event.get_one(id=1)
        md5 = event.md5
        instrument = event.instrument
        request = testing.DummyRequest(
            matchdict={
                'md5': event.md5,
                },
            )
        view = views.EventView(request)
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
        event = sasha.Event.get_one(id=1)
        instrument = event.instrument
        instrument_name = instrument.name.lower().replace(' ', '-')
        instrument_keys = event.fingering.instrument_keys
        instrument_keys = ' '.join(_.name for _ in instrument_keys)
        fingering = event.fingering
        compact_representation = fingering.compact_representation
        request = testing.DummyRequest(
            matchdict={
                'compact_representation': compact_representation,
                'instrument_name': instrument_name,
                },
            )
        view = views.FingeringView(request)
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
        self.assertEqual(info['with_pitch_classes'], '')
        self.assertEqual(info['with_pitches'], '')
        self.assertEqual(info['without_pitch_classes'], '')
        self.assertEqual(info['without_pitches'], '')
        self.assertIsNotNone(info['paginator'])

    def test_HelpView_01(self):
        request = testing.DummyRequest()
        view = views.HelpView(request)
        info = view()
        self.assertEqual(info['body_class'], 'help')
        self.assertEqual(info['title'], 'SASHA | Help')

    def test_HomeView_01(self):
        request = testing.DummyRequest()
        view = views.HomeView(request)
        info = view()
        self.assertEqual(info['body_class'], 'home')
        self.assertEqual(info['title'], 'SASHA | Home')

    def test_InstrumentView_01(self):
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': 'alto-saxophone',
                },
            )
        view = views.InstrumentView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Instrument: Alto Saxophone')

    def test_RandomEventView_01(self):
        request = testing.DummyRequest()
        view = views.RandomEventView(request)
        info = view()
        self.assertEqual(type(info), HTTPFound)
        self.assertIn('/events/', info.location)

    def test_SearchView_01(self):
        request = testing.DummyRequest()
        view = views.SearchView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Search')