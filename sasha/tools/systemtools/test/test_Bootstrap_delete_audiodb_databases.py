from sasha import *    
from sasha.tools.systemtools import Bootstrap


SASHA.environment = 'testing'

def test_Bootstrap_delete_audiodb_databases_01():
    bootstrap = Bootstrap()
    bootstrap.delete_audiodb_databases()
    for name in SASHA['audioDB']:
        assert not AudioDB(name).exists
