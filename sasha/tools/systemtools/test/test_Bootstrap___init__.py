from sasha import *    
from sasha.tools.systemtools import Bootstrap


sasha_configuration.environment = 'testing'

def test_Bootstrap___init___01():
    bootstrap = Bootstrap()
