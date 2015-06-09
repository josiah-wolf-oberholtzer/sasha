import os

from sasha import *    
from sasha.tools.systemtools import Bootstrap


sasha_configuration.environment = 'testing'

def test_Bootstrap_delete_sqlite_database_01():
    bootstrap = Bootstrap()
    bootstrap.create_sqlite_database()
    bootstrap.delete_sqlite_database()
    sqlite_path = os.path.join(sasha_configuration.get_media_path('databases'), sasha_configuration['sqlite']['sqlite'])
    assert not os.path.exists(sqlite_path)    
