import py.test

from sasha import *    
from sasha.tools.systemtools import Bootstrap


SASHA.environment = 'testing'

py.test.skip('Not sure how best to test this yet.')
def test_Bootstrap_populate_sqlite_secondary_01():
    pass
