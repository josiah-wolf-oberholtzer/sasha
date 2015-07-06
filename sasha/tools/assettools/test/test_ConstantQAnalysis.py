from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_ConstantQAnalysis_01():
    event = domaintools.Event.get_one(id=1)
    analysis = assettools.ConstantQAnalysis(event)
    analysis.delete()
    assert not analysis.exists
    analysis.write()
    assert analysis.exists