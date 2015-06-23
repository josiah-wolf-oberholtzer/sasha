from sasha import sasha_configuration
from sasha.tools import domaintools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_sqlite_partials_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()
    bootstrap.populate_sqlite_partials()

    for event in domaintools.Event.get():
        assert len(event.partials)