from sasha import sasha_configuration
from sasha.tools.newdomaintools import Instrument


sasha_configuration.environment = 'testing'


def test_Instrument_01():

    aerophone = Instrument.objects(name='Aerophone').first()
    saxophone = Instrument.objects(name='Saxophone').first()
    alto_saxophone = Instrument.objects(name='Alto Saxophone').first()
    soprano_saxophone = Instrument.objects(name='Soprano Saxophone').first()

    assert aerophone.children == set([
        saxophone,
        alto_saxophone,
        soprano_saxophone,
        ])
    assert aerophone.key_names == []
    assert aerophone.name == 'Aerophone'
    assert aerophone.parents == []
    assert aerophone.transposition == 0

    assert saxophone.children == set([
        alto_saxophone,
        soprano_saxophone,
        ])
    assert saxophone.key_names == []
    assert saxophone.name == 'Saxophone'
    assert saxophone.parents == [aerophone]
    assert saxophone.transposition == 0

    assert alto_saxophone.children == set()
    assert alto_saxophone.key_names == [
        u'8va',
        u'B',
        u'Bf',
        u'Bis',
        u'C',
        u'C1',
        u'C2',
        u'C3',
        u'C4',
        u'C5',
        u'C6',
        u'Cs',
        u'Ef',
        u'Gs',
        u'L1',
        u'L2',
        u'L3',
        u'LowA',
        u'R1',
        u'R2',
        u'R3',
        u'Ta',
        u'Tc',
        u'Tf',
        u'X',
        ]
    assert alto_saxophone.name == 'Alto Saxophone'
    assert alto_saxophone.parents == [saxophone, aerophone]
    assert alto_saxophone.transposition == 3

    assert soprano_saxophone.children == set()
    assert soprano_saxophone.key_names == [
        u'8va',
        u'B',
        u'Bf',
        u'Bis',
        u'C',
        u'C1',
        u'C2',
        u'C3',
        u'C4',
        u'C5',
        u'C6',
        u'Cs',
        u'Ef',
        u'Gs',
        u'L1',
        u'L2',
        u'L3',
        u'LowA',
        u'R1',
        u'R2',
        u'R3',
        u'Ta',
        u'Tc',
        u'Tf',
        u'X',
        ]
    assert soprano_saxophone.name == 'Soprano Saxophone'
    assert soprano_saxophone.parents == [saxophone, aerophone]
    assert soprano_saxophone.transposition == -2