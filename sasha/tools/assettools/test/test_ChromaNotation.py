import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import newdomaintools


sasha_configuration.environment = 'testing'


def test_ChromaNotation_01():
    event = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    plugin = assettools.ChromaNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists


def test_ChromaNotation_02():
    event_a = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.ChromaNotation(event_a)
    analysis_b = assettools.ChromaNotation(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chroma.png'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'event__{}__chroma.png'.format(event_b.md5),
        )