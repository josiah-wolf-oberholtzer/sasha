from sasha import sasha_configuration
from sasha.tools import modeltools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_mongodb_primary_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_mongodb_database()

    event_count = modeltools.Event.objects.count()
    instrument_count = modeltools.Instrument.objects.count()
    performer_count = modeltools.Performer.objects.count()

    assert 0 == event_count
    assert 0 == instrument_count
    assert 0 == performer_count

    bootstrap.create_mongodb_database()
    bootstrap.populate_mongodb_primary()

    event_count = modeltools.Event.objects.count()
    instrument_count = modeltools.Instrument.objects.count()
    performer_count = modeltools.Performer.objects.count()

    assert 0 < event_count
    assert 0 < instrument_count
    assert 0 < performer_count

    event_fixtures = sasha_configuration.get_fixtures(
        modeltools.Event)
    instrument_fixtures = sasha_configuration.get_fixtures(
        modeltools.Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(
        modeltools.Performer)

    assert len(event_fixtures) == event_count
    assert len(instrument_fixtures) == instrument_count
    assert len(performer_fixtures) == performer_count

    bootstrap.rebuild_mongodb_database()