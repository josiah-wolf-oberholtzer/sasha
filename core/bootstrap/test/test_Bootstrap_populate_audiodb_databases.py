from sasha import *    
from sasha.core.bootstrap import Bootstrap
from sasha.core.wrappers import AudioDB


SASHA.environment = 'testing'

def test_Bootstrap_populate_audiodb_databases_01():

    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    event_count = SASHA.get_session().query(Event).count()
    assert 0 < event_count

    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()
    bootstrap.populate_audiodb_databases()

    for name in SASHA['audioDB']:
        adb = AudioDB(name)
        assert adb.status['num_files'] == event_count
