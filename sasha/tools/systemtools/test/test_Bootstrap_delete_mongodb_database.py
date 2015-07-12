from sasha import sasha_configuration
from sasha.tools import models
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_delete_mongodb_database_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_mongodb_database()

    event_count = models.Event.objects.count()
    instrument_count = models.Instrument.objects.count()
    performer_count = models.Performer.objects.count()

    assert 0 == event_count
    assert 0 == instrument_count
    assert 0 == performer_count

    bootstrap.rebuild_mongodb_database()