from sasha import sasha_configuration
from sasha.tools import systemtools
from sasha.tools import wrappertools


sasha_configuration.environment = 'testing'


def test_Bootstrap_delete_audiodb_databases_01():

    assert wrappertools.AudioDB('chroma').exists
    assert wrappertools.AudioDB('constant_q').exists
    assert wrappertools.AudioDB('mfcc').exists

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_audiodb_databases()
    assert not wrappertools.AudioDB('chroma').exists
    assert not wrappertools.AudioDB('constant_q').exists
    assert not wrappertools.AudioDB('mfcc').exists
    bootstrap.create_audiodb_databases()

    assert wrappertools.AudioDB('chroma').exists
    assert wrappertools.AudioDB('constant_q').exists
    assert wrappertools.AudioDB('mfcc').exists