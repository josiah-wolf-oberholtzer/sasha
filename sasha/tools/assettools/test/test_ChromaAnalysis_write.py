from sasha import *
from sasha.tools.assettools import *


SASHA.env = 'testing'

def test_ChromaAnalysis_write_01():
    event = SASHA.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    analysis = ChromaAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists
