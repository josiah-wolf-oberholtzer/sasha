from sasha import sasha_configuration
from sasha.tools import domaintools
from sasha.tools import newdomaintools


sasha_configuration.environment = 'testing'


def test_SashaConfiguration_get_fixtures_01():

    event_fixtures = sasha_configuration.get_fixtures(
        domaintools.Event)
    instrument_fixtures = sasha_configuration.get_fixtures(
        domaintools.Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(
        domaintools.Performer)

    assert len(event_fixtures) == 12
    assert len(instrument_fixtures) == 4
    assert len(performer_fixtures) == 1

    event_fixtures = sasha_configuration.get_fixtures(
        newdomaintools.Event)
    instrument_fixtures = sasha_configuration.get_fixtures(
        newdomaintools.Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(
        newdomaintools.Performer)

    assert len(event_fixtures) == 12
    assert len(instrument_fixtures) == 4
    assert len(performer_fixtures) == 1