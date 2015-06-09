from sasha import *
from sasha.tools.assettools import *


sasha_configuration.env = 'testing'

def test_ChromaNotation_write_01():
    event = sasha_configuration.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    plugin = ChromaNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists
