import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import newdomaintools


sasha_configuration.environment = 'testing'


def test_LogHarmonicityAnalysis_01():
    event = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    analysis = assettools.ChromaAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_LogHarmonicityAnalysis_02():
    event_a = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.LogHarmonicityAnalysis(event_a)
    analysis_b = assettools.LogHarmonicityAnalysis(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.log_harmonicity'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.log_harmonicity'.format(event_b.md5),
        )