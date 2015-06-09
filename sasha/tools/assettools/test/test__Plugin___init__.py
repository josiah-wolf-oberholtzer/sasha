import py.test

from sasha import *
from sasha.tools.assettools._Plugin import _Plugin


sasha_configuration.environment = 'testing'

def test__Plugin___init___01():
    event = Event.get(id=1)[0]
    plugin = _Plugin(event)
    assert plugin.client == event


def test__Plugin___init___02():
    event = Event.get(id=1)[0]
    plugin = _Plugin(1)
    assert event.id == plugin.client.id
    

def test__Plugin___init___03():
    event = Event.get(id=1)[0]
    plugin = _Plugin(event.name)
    assert event.id == plugin.client.id


def test__Plugin___init___04():
    event = Event.get(id=1)[0]
    plugin = _Plugin(event)
    other = _Plugin(plugin)
    assert other.client == plugin.client


def test__Plugin___init___05():
    fingering = Fingering.get(id=1)[0]
    py.test.raises(ValueError, "plugin = _Plugin(fingering)")
