from sasha import sasha_configuration
from sasha.tools import domaintools
from sasha.tools import systemtools
from sasha.tools import wrappertools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_audiodb_databases_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    event_class = domaintools.Event
    event_count = sasha_configuration.get_session().query(event_class).count()
    assert 0 < event_count

    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()
    bootstrap.populate_audiodb_databases()

    adb = wrappertools.AudioDB('chroma')
    assert adb.status['num_files'] == event_count

    adb = wrappertools.AudioDB('constant_q')
    assert adb.status['num_files'] == event_count

    adb = wrappertools.AudioDB('mfcc')
    assert adb.status['num_files'] == event_count