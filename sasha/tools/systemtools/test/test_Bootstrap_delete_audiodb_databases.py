from sasha import sasha_configuration
from sasha.tools import systemtools
from sasha.tools import executabletools


sasha_configuration.environment = 'testing'


def test_Bootstrap_delete_audiodb_databases_01():

    assert executabletools.AudioDB('chroma').exists
    assert executabletools.AudioDB('constant_q').exists
    assert executabletools.AudioDB('mfcc').exists

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_audiodb_databases()
    assert not executabletools.AudioDB('chroma').exists
    assert not executabletools.AudioDB('constant_q').exists
    assert not executabletools.AudioDB('mfcc').exists
    bootstrap.create_audiodb_databases()

    assert executabletools.AudioDB('chroma').exists
    assert executabletools.AudioDB('constant_q').exists
    assert executabletools.AudioDB('mfcc').exists