import os

from sasha import *    
from sasha.tools.systemtools import Bootstrap


SASHA.environment = 'testing'

def test_Bootstrap_create_sqlite_database_01():
    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    sqlite_path = os.path.join(SASHA.get_media_path('databases'), SASHA['sqlite']['sqlite'])
    assert os.path.exists(sqlite_path)
