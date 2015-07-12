# -*- encoding: utf-8 -*-
from pyramid import testing
import sasha
import unittest


class EventTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_Event_01(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        self.assertEqual(event.name, 'event__alto_saxophone__br_042.aif')
        self.assertEqual(event.md5, 'bae113a08990072eb1bfd9c85b8cce34')
        self.assertEqual(event.fingering.instrument.name, 'Alto Saxophone')
        self.assertEqual(
            event.fingering.compact_representation,
            '0010000000001010001110000',
            )

    def test_Event_get_md5_link(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        request = testing.DummyRequest(matchdict={'md5': event.md5})
        link = event.get_md5_link(request)
        self.assertEqual(
            link.encode('utf-8'),
            '<a href="http://example.com/events/bae113a08990072eb1bfd9c85b8cce34/">bae113a08990072eb1bfd9c85b8cce34</a>',
            )

    def test_Event_get_numbered_link(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        request = testing.DummyRequest(matchdict={'md5': event.md5})
        link = event.get_numbered_link(request)
        self.assertEqual(
            link.encode('utf-8'),
            '<a href="http://example.com/events/bae113a08990072eb1bfd9c85b8cce34/">Event № 5b8cce34</a>',
            )

    def test_Event_get_url(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        request = testing.DummyRequest(matchdict={'md5': event.md5})
        url = event.get_url(request)
        self.assertEqual(
            url,
            'http://example.com/events/bae113a08990072eb1bfd9c85b8cce34/',
            )

    def test_Event_canonical_event_name(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        self.assertEqual(
            event.canonical_event_name,
            'event__bae113a08990072eb1bfd9c85b8cce34',
            )

    def test_Event_canonical_fingering_name(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        self.assertEqual(
            event.canonical_fingering_name,
            'fingering__alto_saxophone__0010000000001010001110000',
            )

    def test_Event_link_text(self):
        event = sasha.models.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        self.assertEqual(event.link_text, 'Event № 5b8cce34')