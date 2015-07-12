from sasha import sasha_configuration
from sasha.tools import models


sasha_configuration.environment = 'testing'


def test_Event_query_audiodb_01():
    event = models.Event.objects[0]
    result = event.query_audiodb('chroma', limit=10)
    assert result


def test_Event_query_audiodb_02():
    event = models.Event.objects[0]
    result = event.query_audiodb('constant_q', limit=10)
    assert result


def test_Event_query_audiodb_03():
    event = models.Event.objects[0]
    result = event.query_audiodb('mfcc', limit=10)
    assert result