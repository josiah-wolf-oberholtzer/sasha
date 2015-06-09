from sasha import *
from sasha.plugins import *


SASHA.env = 'testing'

def test_ChromaNotation_write_01():
    event = SASHA.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    plugin = ChromaNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists
