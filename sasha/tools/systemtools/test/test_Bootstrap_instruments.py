from sasha import sasha_configuration
from sasha.tools import models
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_instruments_01():

    bootstrap = systemtools.Bootstrap()
    fixtures = sasha_configuration.get_fixtures(models.Instrument)
    assert fixtures
    fixtures = bootstrap._sort_instrument_fixtures(fixtures)
    assert fixtures
    mapping = bootstrap._collect_instrument_parents(fixtures)
    assert mapping == {
        u'Aerophone': [],
        u'Saxophone': [u'Aerophone'],
        u'Alto Saxophone': [u'Saxophone', u'Aerophone'],
        u'Soprano Saxophone': [u'Saxophone', u'Aerophone'],
        }