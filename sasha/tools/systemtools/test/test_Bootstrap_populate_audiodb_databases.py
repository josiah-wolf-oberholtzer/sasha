from sasha import *    
from sasha.tools.systemtools import Bootstrap
from sasha.tools.wrappertools import AudioDB


sasha_configuration.environment = 'testing'

def test_Bootstrap_populate_audiodb_databases_01():

    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    event_count = sasha_configuration.get_session().query(Event).count()
    assert 0 < event_count

    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()
    bootstrap.populate_audiodb_databases()

    for name in sasha_configuration['audioDB']:
        adb = AudioDB(name)
        assert adb.status['num_files'] == event_count
