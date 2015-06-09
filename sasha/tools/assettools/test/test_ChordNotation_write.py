from sasha import *
from sasha.tools.assettools import *


sasha_configuration.env = 'testing'

def test_ChordNotation_write_01():
    event = sasha_configuration.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    plugin = ChordNotation(event)
    plugin.delete()
    assert all([not x for x in plugin.exists.values()])
    plugin.write()
    assert all([x for x in plugin.exists.values()])
