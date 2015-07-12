import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import models


sasha_configuration.environment = 'testing'


def test_ConstantQAnalysis_01():
    event = models.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    analysis = assettools.ConstantQAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_ConstantQAnalysis_02():
    event_a = models.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = models.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.ConstantQAnalysis(event_a)
    analysis_b = assettools.ConstantQAnalysis(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.constant_q'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.constant_q'.format(event_b.md5),
        )