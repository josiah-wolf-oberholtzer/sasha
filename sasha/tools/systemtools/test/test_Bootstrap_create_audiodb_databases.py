import os
from sasha import sasha_configuration
from sasha.tools import systemtools
from sasha.tools import executabletools


sasha_configuration.environment = 'testing'


def test_Bootstrap_create_audiodb_databases_01():

    executable = executabletools.AudioDB('chroma').executable
    executable = os.path.abspath(executable)
    print executable, os.path.exists(executable)

    print executabletools.AudioDB('chroma').path
    print executabletools.AudioDB('constant_q').path
    print executabletools.AudioDB('mfcc').path

    #assert executabletools.AudioDB('chroma').exists
    #assert executabletools.AudioDB('constant_q').exists
    #assert executabletools.AudioDB('mfcc').exists

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()

    assert executabletools.AudioDB('chroma').exists
    assert executabletools.AudioDB('constant_q').exists
    assert executabletools.AudioDB('mfcc').exists