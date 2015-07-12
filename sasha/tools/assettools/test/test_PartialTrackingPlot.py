import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import modeltools


sasha_configuration.environment = 'testing'


def test_PartialTrackingPlot_01():
    event = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    plugin = assettools.PartialTrackingPlot(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists


def test_PartialTrackingPlot_02():
    event_a = modeltools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    event_b = modeltools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    analysis_a = assettools.PartialTrackingPlot(event_a)
    analysis_b = assettools.PartialTrackingPlot(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('plots'),
        'event__{}__partials.png'.format(event_a.md5),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('plots'),
        'event__{}__partials.png'.format(event_b.md5),
        )