from sasha import *
from sasha.tools.assettools import *


sasha_configuration.environment = 'testing'

def test_LogHarmonicityAnalysis_01():
    event = sasha_configuration.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    analysis = ChromaAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists
