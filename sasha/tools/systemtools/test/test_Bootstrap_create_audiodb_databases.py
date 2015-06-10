from sasha import *
from sasha.tools.systemtools import Bootstrap


sasha_configuration.environment = 'testing'


def test_Bootstrap_create_audiodb_databases_01():

    bootstrap = Bootstrap()
    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()

    assert AudioDB('chroma').exists
    assert AudioDB('constant_q').exists
    assert AudioDB('mfcc').exists