import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_PartialTrackingPlot_01():
    event = domaintools.Event.get_one(id=1)
    plugin = assettools.PartialTrackingPlot(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists


def test_PartialTrackingPlot_02():
    event_a = domaintools.Event.get_one(id=1)
    event_b = domaintools.Event.get_one(id=2)
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