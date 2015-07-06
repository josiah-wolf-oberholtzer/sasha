from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_ChordNotation_01():
    event = domaintools.Event.get_one(id=1)
    plugin = assettools.ChordNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists