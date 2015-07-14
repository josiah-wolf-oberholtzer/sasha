from pyramid import testing
from sasha.tools import viewtools
import sasha
import unittest


class FingeringViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

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