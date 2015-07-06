import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_ChromaAnalysis_01():
    event = domaintools.Event.get_one(id=1)
    analysis = assettools.ChromaAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_ChromaAnalysis_02():
    event_a = domaintools.Event.get_one(id=1)
    event_b = domaintools.Event.get_one(id=2)
    analysis_a = assettools.ChromaAnalysis(event_a)
    analysis_b = assettools.ChromaAnalysis(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.chroma'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.chroma'.format(event_b.md5),
        )