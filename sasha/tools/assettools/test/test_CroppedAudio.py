import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_CroppedAudio_01():
    event = domaintools.Event.get_one(id=1)
    analysis = assettools.CroppedAudio(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_CroppedAudio_02():
    event_a = domaintools.Event.get_one(id=1)
    event_b = domaintools.Event.get_one(id=2)
    analysis_a = assettools.CroppedAudio(event_a)
    analysis_b = assettools.CroppedAudio(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('source_audio'),
        'event__{}__cropped.aif'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('source_audio'),
        'event__{}__cropped.aif'.format(event_b.md5),
        )