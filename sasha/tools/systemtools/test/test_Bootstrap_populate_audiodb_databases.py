from sasha import sasha_configuration
from sasha.tools import executabletools
from sasha.tools import modeltools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_audiodb_databases_01():

    bootstrap = systemtools.Bootstrap()

    event_count = modeltools.Event.objects.count()
    assert 0 < event_count

    assert executabletools.AudioDB('chroma').exists
    assert executabletools.AudioDB('constant_q').exists
    assert executabletools.AudioDB('mfcc').exists

    bootstrap.delete_audiodb_databases()
    bootstrap.create_audiodb_databases()
    bootstrap.populate_audiodb_databases()

    assert executabletools.AudioDB('chroma').exists
    assert executabletools.AudioDB('constant_q').exists
    assert executabletools.AudioDB('mfcc').exists

    adb = executabletools.AudioDB('chroma')
    assert adb.status['num_files'] == event_count

    adb = executabletools.AudioDB('constant_q')
    assert adb.status['num_files'] == event_count

    adb = executabletools.AudioDB('mfcc')
    assert adb.status['num_files'] == event_count