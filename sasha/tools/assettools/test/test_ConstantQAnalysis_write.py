from sasha import *
from sasha.tools.assettools import *


sasha_configuration.environment = 'testing'

def test_ConstantQAnalysis_write_01():
    event = sasha_configuration.get_session().query(Event).order_by('RANDOM()').limit(1).all()[0]
    analysis = ConstantQAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists