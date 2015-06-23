import os
from sasha import sasha_configuration
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_create_sqlite_database_01():
    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    sqlite_path = os.path.join(
        sasha_configuration.get_media_path('databases'),
        sasha_configuration['sqlite']['sqlite'],
        )
    assert os.path.exists(sqlite_path)