import os

from sasha import *    
from sasha.core.bootstrap import Bootstrap


SASHA.environment = 'testing'

def test_Bootstrap_delete_sqlite_database_01():
    bootstrap = Bootstrap()
    bootstrap.create_sqlite_database()
    bootstrap.delete_sqlite_database()
    sqlite_path = os.path.join(SASHA.get_media_path('databases'), SASHA['sqlite']['sqlite'])
    assert not os.path.exists(sqlite_path)    
