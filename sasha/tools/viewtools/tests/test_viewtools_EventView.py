from pyramid import testing
from sasha.tools import viewtools
import sasha
import unittest


class EventViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

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