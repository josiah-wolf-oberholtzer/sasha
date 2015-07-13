import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import modeltools


sasha_configuration.environment = 'testing'


def test_ChromaNotation_01():
    event = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    asset = assettools.ChromaNotation(event)
    asset.delete()
    assert not asset.exists
    asset.write()
    assert asset.exists


def test_ChromaNotation_02():
    event_a = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = modeltools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.ChromaNotation(event_a)
    analysis_b = assettools.ChromaNotation(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chroma.svg'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chroma.svg'.format(event_b.md5),
        )