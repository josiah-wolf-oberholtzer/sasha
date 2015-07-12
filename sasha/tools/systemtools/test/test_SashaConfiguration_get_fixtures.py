from sasha import sasha_configuration
from sasha.tools import models


sasha_configuration.environment = 'testing'


def test_SashaConfiguration_get_fixtures_01():

    event_fixtures = sasha_configuration.get_fixtures(
        models.Event)
    instrument_fixtures = sasha_configuration.get_fixtures(
        models.Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(
        models.Performer)

    assert len(event_fixtures) == 12
    assert len(instrument_fixtures) == 4
    assert len(performer_fixtures) == 1