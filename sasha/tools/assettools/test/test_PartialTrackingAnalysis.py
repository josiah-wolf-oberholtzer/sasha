import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import models


sasha_configuration.environment = 'testing'


def test_PartialTrackingAnalysis_01():
    event = models.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    analysis = assettools.PartialTrackingAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists


def test_PartialTrackingAnalysis_02():
    event_a = models.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = models.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.PartialTrackingAnalysis(event_a)
    analysis_b = assettools.PartialTrackingAnalysis(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.partials'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('analyses'),
        'event__{}.partials'.format(event_b.md5),
        )