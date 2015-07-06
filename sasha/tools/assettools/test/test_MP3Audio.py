from sasha import *
from sasha.tools.assettools import *


sasha_configuration.environment = 'testing'

def test_MP3Audio_01():
    event = sasha_configuration.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    plugin = MP3Audio(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists
