import py.test

from sasha import *
from sasha.tools.assettools.Asset import Asset


sasha_configuration.environment = 'testing'

def test_Asset_01():
    event = Event.get(id=1)[0]
    plugin = Asset(event)
    assert plugin.client == event


def test_Asset_02():
    event = Event.get(id=1)[0]
    plugin = Asset(1)
    assert event.id == plugin.client.id
    

def test_Asset_03():
    event = Event.get(id=1)[0]
    plugin = Asset(event.name)
    assert event.id == plugin.client.id


def test_Asset_04():
    event = Event.get(id=1)[0]
    plugin = Asset(event)
    other = Asset(plugin)
    assert other.client == plugin.client


def test_Asset_05():
    fingering = Fingering.get(id=1)[0]
    py.test.raises(ValueError, "plugin = Asset(fingering)")