from pyramid.httpexceptions import HTTPFound
from pyramid import testing
import unittest
import sasha
from sashaweb import views


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('sashaweb')

    def tearDown(self):
        testing.tearDown()

    def test_ClusterView_01(self):
        cluster = sasha.Cluster.get_one(id=1)
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        view = views.SingleClusterView(request)
        info = view()
        self.assertEqual(info['body_class'], 'clusters')
        self.assertEqual(info['title'], 'SASHA | Chroma Cluster No.1')

    def test_EventView_01(self):
        event = sasha.Event.get_one(id=1)
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
            'SASHA | Alto Saxophone Event: c5c19c1eb8b2fd2fa5d3e18566f10b3e',
            )

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

    def test_SingleFingeringView_01(self):
        event = sasha.Event.get_one(id=1)
        instrument = event.instrument
        instrument_name = instrument.name.lower().replace(' ', '-')
        fingering = event.fingering
        compact_representation = fingering.compact_representation
        request = testing.DummyRequest(
            matchdict={
                'compact_representation': compact_representation,
                'instrument_name': instrument_name,
                },
            )
        view = views.SingleFingeringView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['fingering'].id, fingering.id)
        self.assertEqual(
            set(_.id for _ in info['fingerings']),
            set(_.id for _ in fingering.find_similar_fingerings(12)),
            )
        self.assertEqual(info['instrument'].id, instrument.id)
        self.assertEqual(info['instrument_keys'], 'C Ef L1 L2 L3 R1 R3')
        self.assertEqual(info['instrument_name'], 'Alto Saxophone')
        self.assertEqual(
            info['search_action'],
            'http://example.com/instruments/alto-saxophone/0000100000001011101010000/'
            )
        self.assertEqual(
            info['title'],
            'SASHA | Alto Saxophone Fingering: C Ef L1 L2 L3 R1 R3',
            )
        self.assertEqual(info['with_pitch_classes'], '')
        self.assertEqual(info['with_pitches'], '')
        self.assertEqual(info['without_pitch_classes'], '')
        self.assertEqual(info['without_pitches'], '')
        self.assertIsNotNone(info['paginator'])

    def test_SingleInstrumentView_01(self):
        request = testing.DummyRequest(
            matchdict={
                'instrument_name': 'alto-saxophone',
                },
            )
        view = views.SingleInstrumentView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Instrument: Alto Saxophone')