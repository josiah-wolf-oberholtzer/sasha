import os

from abjad.tools.pitchtools import NamedChromaticPitch
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from sasha import SASHACFG
from sasha.core.bootstrap._get_fixtures import _get_fixtures
from sasha.core.domain import *
from sasha.plugins import SourceAudio
from sasha.plugins import ChordAnalysis


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

    # INSTRUMENTS, KEYS
    for fixture in fixtures['instruments']:
        data = fixture['main']
        instrument = Instrument(name=data['name'])
        session.add(instrument)
        instrument_keys = filter(None, data['idiom_schema'].split(' '))
        for instrument_key in instrument_keys:
            session.add(InstrumentKey(name=instrument_key, instrument=instrument))
    for fixture in fixtures['instruments']:
        data = fixture['main']
        if data['parent_name']:
            child = session.query(Instrument).filter_by(name=data['name']).one( )
            parent = session.query(Instrument).filter_by(name=data['parent_name']).one( )
            child.parent = parent
    
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
        fingering.compact_representation = fingering._generate_compact_representation( )
        session.add(fingering)

        event = Event(fingering=fingering, instrument=instrument, name=name, performer=performer)

        md5 = SourceAudio(event).md5
        if Event.get(md5=md5):
            raise Exception('Duplicate MD5 found.')
        event.md5 = md5
    
        session.add(event)

        chord = ChordAnalysis(event).read( )
        for pitch_number, amplitude in chord:
            pitch = NamedChromaticPitch(pitch_number)
            pitch_class_number = pitch.chromatic_pitch_class_number
            octave_number = pitch.octave_number
            session.add(Partial(event=event,
                pitch_number=pitch_number,
                pitch_class_number=pitch_class_number,
                octave_number=octave_number))

    session.commit( )