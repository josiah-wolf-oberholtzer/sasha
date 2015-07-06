import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_LinearSpectrumAnalysis_01():
    event = domaintools.Event.get_one(id=1)
    analysis = assettools.LinearSpectrumAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_LinearSpectrumAnalysis_02():
    event_a = domaintools.Event.get_one(id=1)
    event_b = domaintools.Event.get_one(id=2)
    analysis_a = assettools.LinearSpectrumAnalysis(event_a)
    analysis_b = assettools.LinearSpectrumAnalysis(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.linear_spectrum'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.linear_spectrum'.format(event_b.md5),
        )