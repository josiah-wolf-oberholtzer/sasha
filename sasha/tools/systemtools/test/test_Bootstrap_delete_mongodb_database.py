from sasha import sasha_configuration
from sasha.tools import newdomaintools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_mongodb_primary_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_mongodb_database()

    event_count = newdomaintools.Event.objects.count()
    instrument_count = newdomaintools.Instrument.objects.count()
    performer_count = newdomaintools.Performer.objects.count()

    assert 0 == event_count
    assert 0 == instrument_count
    assert 0 == performer_count