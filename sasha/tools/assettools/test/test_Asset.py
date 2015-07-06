import py.test
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_assettools.Asset_01():
    event = domaintools.Event.get(id=1)[0]
    plugin = assettools.Asset(event)
    assert plugin.client == event


def test_assettools.Asset_02():
    event = domaintools.Event.get(id=1)[0]
    plugin = assettools.Asset(1)
    assert event.id == plugin.client.id


def test_assettools.Asset_03():
    event = domaintools.Event.get(id=1)[0]
    plugin = assettools.Asset(event.name)
    assert event.id == plugin.client.id


def test_assettools.Asset_04():
    event = domaintools.Event.get(id=1)[0]
    plugin = assettools.Asset(event)
    other = assettools.Asset(plugin)
    assert other.client == plugin.client


def test_assettools.Asset_05():
    fingering = domaintools.Fingering.get(id=1)[0]
    py.test.raises(ValueError, "plugin = assettools.Asset(fingering)")