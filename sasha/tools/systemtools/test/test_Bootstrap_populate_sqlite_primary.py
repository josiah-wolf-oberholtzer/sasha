from sasha import sasha_configuration
from sasha.tools import domaintools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_sqlite_primary_01():
    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    session = sasha_configuration.get_session()

    assert 0 < len(domaintools.Event.get())
    assert 0 < len(domaintools.Instrument.get())
    assert 0 < len(domaintools.Performer.get())

    event_fixtures = sasha_configuration.get_fixtures(domaintools.Event)
    instrument_fixtures = sasha_configuration.get_fixtures(domaintools.Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(domaintools.Performer)

    assert len(event_fixtures) == session.query(domaintools.Event).count()
    assert len(instrument_fixtures) == session.query(domaintools.Instrument).count()
    assert len(performer_fixtures) == session.query(domaintools.Performer).count()