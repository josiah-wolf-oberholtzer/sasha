from sasha import *
from sasha.plugins import SourceAudio


def _populate_sqlite_primary( ):

    SASHA.logger.info('Populating SQLite primary objects.')

    session = SASHA.get_session( )

    # PERFORMERS
    for fixture in Performer.get_fixtures( ):
        data = fixture['main']
        session.add(Performer(name=data['name']))

    # INSTRUMENTS, KEYS
    for fixture in Instrument.get_fixtures( ):
        data = fixture['main']
        instrument = Instrument(name=data['name'])
        session.add(instrument)
        instrument_keys = filter(None, data['idiom_schema'].split(' '))
        for instrument_key in instrument_keys:
            session.add(InstrumentKey(name=instrument_key, instrument=instrument))
    for fixture in Instrument.get_fixtures( ):
        data = fixture['main']
        if data['parent_name']:
            child = session.query(Instrument).filter_by(name=data['name']).one( )
            parent = session.query(Instrument).filter_by(name=data['parent_name']).one( )
            child.parent = parent

    # EVENTS, FINGERINGS
    for fixture in Event.get_fixtures( ):
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

        # check if the fingering already exists
        extant_fingering = Fingering.get(instrument=instrument,
            compact_representation=compact_representation)
        if not extant_fingering:
            session.add(fingering)
        else:
            fingering = extant_fingering[0]

        event = Event(fingering=fingering,
            instrument=instrument,
            name=name,
            performer=performer)

        md5 = SourceAudio(event).md5
        event.md5 = md5

        session.add(event)

    session.commit( )
