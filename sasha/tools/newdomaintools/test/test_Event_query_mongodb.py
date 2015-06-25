from sasha import sasha_configuration
from sasha.tools import newdomaintools


sasha_configuration.environment = 'testing'


def test_Event_query_mongodb_01():
    r'''By instrument.'''
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__alto_saxophone__kientzy_47__t2.aif',
        u'event__alto_saxophone__kientzy_47__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Soprano Saxophone',
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__soprano_saxophone__br_073.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]


def test_Event_query_mongodb_02():
    r'''With pitches.'''
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[15],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_47__t2.aif',
        u'event__alto_saxophone__kientzy_47__t3.aif',
        u'event__soprano_saxophone__br_073.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[15, 24],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_47__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[15, 24, 30],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_47__t3.aif',
        ]


def test_Event_query_mongodb_03():
    r'''Without pitches.'''
    events = newdomaintools.Event.query_mongodb(
        without_pitches=[24],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__alto_saxophone__kientzy_47__t2.aif',
        u'event__soprano_saxophone__br_073.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        without_pitches=[15, 24],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        without_pitches=[8.5, 15, 24],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]


def test_Event_query_mongodb_04():
    r'''With and without pitches.'''
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[15],
        without_pitches=[8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__soprano_saxophone__br_073.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[15],
        without_pitches=[8.5, 23],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitches=[8, 15],
        without_pitches=[8.5, 23],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        ]


def test_Event_query_mongodb_05():
    r'''With pitch-classes.'''
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_47__t2.aif',
        u'event__alto_saxophone__kientzy_47__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[1.5, 8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[1.5, 5, 8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_123.aif',
        ]


def test_Event_query_mongodb_06():
    r'''Without pitch-classes.'''
    events = newdomaintools.Event.query_mongodb(
        without_pitch_classes=[8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__soprano_saxophone__br_073.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        without_pitch_classes=[0, 8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__soprano_saxophone__br_073.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        without_pitch_classes=[0, 3, 8.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        u'event__alto_saxophone__kientzy_47__t1.aif',
        u'event__soprano_saxophone__chromatic_scale_a4.aif',
        ]


def test_Event_query_mongodb_07():
    r'''With and without pitch-classes.'''
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[8.5],
        without_pitch_classes=[6],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_47__t2.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[1.5, 8.5],
        without_pitch_classes=[6],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        with_pitch_classes=[1.5, 8.5],
        without_pitch_classes=[6, 10.5],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        ]


def test_Event_query_mongodb_08():
    r'''With keys.'''
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf', 'Ef'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf', 'Ef', 'L2'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        ]


def test_Event_query_mongodb_09():
    r'''Without keys.'''
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        without_keys=['Bis'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
        u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        without_keys=['8va', 'Bis'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        without_keys=['8va', 'Bis', 'L2'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        ]


def test_Event_query_mongodb_10():
    r'''With and without keys.'''
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf'],
        without_keys=['8va'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        u'event__alto_saxophone__kientzy_19__t1.aif',
        u'event__alto_saxophone__kientzy_19__t2.aif',
        u'event__alto_saxophone__kientzy_19__t3.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf', 'R2'],
        without_keys=['8va'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        u'event__alto_saxophone__br_123.aif',
        ]
    events = newdomaintools.Event.query_mongodb(
        instrument_name='Alto Saxophone',
        with_keys=['Bf', 'R2'],
        without_keys=['8va', 'C'],
        ).order_by('name')
    assert list(event.name for event in events) == [
        u'event__alto_saxophone__br_042.aif',
        ]