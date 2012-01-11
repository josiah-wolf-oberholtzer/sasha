import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from sasha import SASHACFG
from sasha.core.bootstrap._get_fixtures import _get_fixtures
from sasha.core.sqldomain import *


def _bootstrap( ):

    fixtures = _get_fixtures( )

    dbpath = os.path.join(SASHACFG.get_media_path('databases'),
        SASHACFG['sqlite3']['sqlalchemy'])    
    engine = create_engine('sqlite:///%s' % dbpath)

    metadata = Event.metadata
    metadata.drop_all(engine)
    metadata.create_all(engine)

    session = SASHACFG.get_session( )

    # PERFORMERS
    for fixture in fixtures['performers']:
        data = fixture['main']
        session.add(Performer(name=data['name']))

    session.commit( )

    # INSTRUMENTS, KEYS
    for fixture in fixtures['instruments']:
        data = fixture['main']
        instrument = Instrument(name=data['name'])
        session.add(instrument)
        instrument_keys = filter(None, data['idiom_schema'].split(' '))
        for instrument_key in instrument_keys:
            session.add(InstrumentKey(name=instrument_key, instrument=instrument))

    session.commit( )

    for fixture in fixtures['instruments']:
        data = fixture['main']
        if data['parent_name']:
            child = session.query(Instrument).filter_by(name=data['name']).one( )
            parent = session.query(Instrument).filter_by(name=data['parent_name']).one( )
            child.parent = parent

    session.commit( )
    
    # EVENTS, FINGERINGS
    for fixture in fixtures['events']:
        data = fixture['main']

        instrument = session.query(Instrument).filter_by(name=data['instrument_name']).one( )
        name = data['name']
        performer = session.query(Performer).filter_by(name=data['performer_name']).one( )

        key_names = filter(None, data['idiom'].split(' '))
        instrument_keys = session.query(InstrumentKey).filter(
            InstrumentKey.instrument == instrument).filter(
            InstrumentKey.name.in_(key_names))

        fingering = Fingering(instrument=instrument)
        fingering.instrument_keys.extend(instrument_keys)
        session.add(fingering)

        event = Event(fingering=fingering, instrument=instrument, name=name, performer=performer)
        session.add(event)

    session.commit( )
