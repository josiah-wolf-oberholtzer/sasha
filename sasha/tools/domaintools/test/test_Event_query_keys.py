from sasha import *


sasha_configuration.environment = 'testing'


def test_Event_query_keys_01():
    with_keys = []
    without_keys = []
    query = Event.query_keys('Alto Saxophone', with_keys, without_keys)
    events = list(query)
    assert len(events) == 10
    for event in events:
        assert event.instrument.name == 'Alto Saxophone'


def test_Event_query_keys_02():
    with_keys = ['Bf']
    without_keys = []
    query = Event.query_keys('Alto Saxophone', with_keys, without_keys)
    events = list(query)
    assert len(events) == 7
    for event in events:
        assert event.instrument.name == 'Alto Saxophone'
        key_names = set(_.name for _ in event.fingering.instrument_keys)
        assert 'Bf' in key_names


def test_Event_query_keys_03():
    with_keys = ['Bf', '8va']
    without_keys = []
    query = Event.query_keys('Alto Saxophone', with_keys, without_keys)
    events = list(query)
    assert len(events) == 2
    for event in events:
        assert event.instrument.name == 'Alto Saxophone'
        key_names = set(_.name for _ in event.fingering.instrument_keys)
        assert 'Bf' in key_names
        assert '8va' in key_names


def test_Event_query_keys_04():
    with_keys = ['Bf']
    without_keys = ['R2']
    query = Event.query_keys('Alto Saxophone', with_keys, without_keys)
    events = list(query)
    assert len(events) == 3
    for event in events:
        assert event.instrument.name == 'Alto Saxophone'
        key_names = set(_.name for _ in event.fingering.instrument_keys)
        assert 'Bf' in key_names
        assert 'R2' not in key_names