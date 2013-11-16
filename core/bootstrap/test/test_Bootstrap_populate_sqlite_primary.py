from sasha import *    
from sasha.core.bootstrap import Bootstrap


SASHA.environment = 'testing'

def test_Bootstrap_populate_sqlite_primary_01():
    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    session = SASHA.get_session()
    assert 0 < len(Event.get())
    assert 0 < len(Instrument.get())
    assert 0 < len(Performer.get())
    assert len(Event.get_fixtures()) == session.query(Event).count()
    assert len(Instrument.get_fixtures()) == session.query(Instrument).count()
    assert len(Performer.get_fixtures()) == session.query(Performer).count()
