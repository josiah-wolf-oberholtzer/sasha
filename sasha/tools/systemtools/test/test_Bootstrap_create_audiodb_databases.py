from sasha import sasha_configuration
from sasha.tools import systemtools
from sasha.tools import wrappertools


sasha_configuration.environment = 'testing'


def test_Bootstrap_create_audiodb_databases_01():

    print  wrappertools.AudioDB('chroma').path
    print  wrappertools.AudioDB('constant_q').path
    print  wrappertools.AudioDB('mfcc').path

    assert wrappertools.AudioDB('chroma').exists
    assert wrappertools.AudioDB('constant_q').exists
    assert wrappertools.AudioDB('mfcc').exists

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()

    assert wrappertools.AudioDB('chroma').exists
    assert wrappertools.AudioDB('constant_q').exists
    assert wrappertools.AudioDB('mfcc').exists