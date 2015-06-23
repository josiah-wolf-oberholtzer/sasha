from sasha import *    
from sasha.tools.systemtools import Bootstrap


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_sqlite_primary_01():
    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    session = sasha_configuration.get_session()

    assert 0 < len(Event.get())
    assert 0 < len(Instrument.get())
    assert 0 < len(Performer.get())

    event_fixtures = sasha_configuration.get_fixtures(Event)
    instrument_fixtures = sasha_configuration.get_fixtures(Instrument)
    performer_fixtures = sasha_configuration.get_fixtures(Performer)

    assert len(event_fixtures) == session.query(Event).count()
    assert len(instrument_fixtures) == session.query(Instrument).count()
    assert len(performer_fixtures) == session.query(Performer).count()