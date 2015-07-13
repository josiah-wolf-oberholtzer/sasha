import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import modeltools


sasha_configuration.environment = 'testing'


def test_ChordNotation_01():
    event = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    asset = assettools.ChordNotation(event)
    asset.delete()
    assert not asset.exists
    asset.write()
    assert asset.exists


def test_ChordNotation_02():
    event_a = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = modeltools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.ChordNotation(event_a)
    analysis_b = assettools.ChordNotation(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chord.svg'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chord.svg'.format(event_b.md5),
        )