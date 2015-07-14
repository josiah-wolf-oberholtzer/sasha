# -*- encoding: utf-8 -*-
import unittest
from sasha import sasha_configuration
from sasha.tools import modeltools


class SashaConfigurationTests(unittest.TestCase):

    def setUp(self):
        sasha_configuration.environment = 'testing'

    def tearDown(self):
        pass

    def test_SashaConfiguration_get_fixtures_01(self):

        event_fixtures = sasha_configuration.get_fixtures(
            modeltools.Event)
        instrument_fixtures = sasha_configuration.get_fixtures(
            modeltools.Instrument)
        performer_fixtures = sasha_configuration.get_fixtures(
            modeltools.Performer)

        assert len(event_fixtures) == 12
        assert len(instrument_fixtures) == 4
        assert len(performer_fixtures) == 1