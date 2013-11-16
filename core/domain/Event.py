import os
import shutil

from abjad.tools import stringtools
from abjad.tools import pitchtools
from sqlalchemy import and_, Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

from sasha import SASHA
from sasha.core.domain.DomainObject import DomainObject
from sasha.core.wrappers import AudioDB


class Event(DomainObject):

    __fixture_paths__ = (
        'description',
        'fingering.instrument_keys.name',
        'instrument.name',
        'name',
        'performer.name',
    )

    ### SQLALCHEMY ###

    __table_args__ = (UniqueConstraint('id', 'md5', 'name'), { })

    description = Column(String, nullable=True)
    fingering_id = Column(Integer, ForeignKey('fingerings.id'))
    fingering = relationship('Fingering', backref='events')
    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='events')
    instrument_model_id = Column(Integer, ForeignKey('instrument_models.id'))
    instrument_model = relationship('InstrumentModel', backref='events')
    md5 = Column(String, unique=True)
    name = Column(String, unique=True)
    performer_id = Column(Integer, ForeignKey('performers.id'))
    performer = relationship('Performer', backref='events')
    recording_date = Column(Date, nullable = True)
    recording_location_id = Column(Integer, ForeignKey('recording_locations.id'))
    recording_location = relationship('RecordingLocation', backref='events')

    @declared_attr
    def clusters(cls):
        association_table = Table('cluster_associations',
            cls.metadata,
            Column('event_id', Integer, ForeignKey('events.id')),
            Column('cluster_id', Integer, ForeignKey('clusters.id')))
        return relationship('Cluster',
            secondary=association_table, backref='events')

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%r)>' % (type(self).__name__, str(self.name))

    ### PUBLIC ATTRIBUTES ###

    @property
    def canonical_name(self):
        cls_name = stringtools.upper_camel_case_to_snake_case(type(self).__name__)
        return '%s__%s' % (cls_name, self.md5)

    @property
    def source_audio(self):
        from sasha.plugins.audio import SourceAudio
        return SourceAudio(self)

    @property
    def pitches(self):
        return tuple([pitchtools.NamedPitch(x.pitch_number) for x in self.partials])

    @property
    def pitch_names(self):
        return tuple([x.pitch_name for x in self.pitches])

    @property
    def pitch_classes(self):
        return tuple(set([pitchtools.NamedPitchClass(x.pitch_class_number) for x in self.partials]))

    ### PUBLIC METHODS ###

    def export_assets_to_path(self, destination, klasses=[]):
        name = self.name.partition('.')[0]
        for klass in klasses:
            asset = klass(self)
            if isinstance(asset.path, str):
                newname = os.path.basename(asset.path).replace(self.canonical_name, name)
                shutil.copy(asset.path, os.path.join(destination, newname))
            elif isinstance(asset.path, dict):
                for path in asset.path.values():
                    newname = os.path.basename(path).replace(self.canonical_name, name)
                    shutil.copy(path, os.path.join(destination, newname))

    @classmethod
    def from_canonical_name_prefix(cls, name):
        parts = name.split('__')
        cls_name = underscore_delimited_lowercase_to_stringtools.uppercamelcase(parts[0])
        if cls_name != cls.__name__:
            return None
        return cls.get(md5=parts[1])[0]

    def query_audiodb(self, method, limit = 10):
        '''Query events matched against an Event instance via `method`:

        ::

            >>> event = Event.get_one(id=1)
            >>> result = event.query_audiodb('mfcc', limit=10)

        Returns list of 2-tuples, of Event and matching frames.
        '''
        from sasha.core.wrappers import AudioDB
        assert isinstance(limit, int) and 0 < limit
        if method in SASHA['audioDB']:
            adb = AudioDB(method)
            return adb.query(self, limit)
        else:
            raise ValueError('Unknown search method "%s".' % repr(method))

    @staticmethod
    def query_keys(instrument_name, with_keys = [ ], without_keys = [ ]):
        '''Query events with and without keys:

        ::

            >>> instrument_name = Instrument.get_one('Alto Saxophone').name
            >>> with_keys = [ ]
            >>> without_keys = [ ]
            >>> query = Event.query_keys(instrument_name, with_keys, without_keys)

        Returns SQLAlchemy Query instance.
        '''
        from sasha.core.domain import Fingering, Instrument, InstrumentKey
        instrument = Instrument.get(name=instrument_name)[0]
        query = SASHA.get_session().query(Event).\
            filter_by(instrument=instrument).\
            join('fingering', 'instrument_keys').\
            join(Instrument)

        with_query = None
        if with_keys:
            to_intersect = [query.filter(InstrumentKey.name.in_([key])) for key in with_keys]
            with_query = query.intersect(*to_intersect).distinct()

        without_query = None
        if without_keys:
            without_query = query.filter(InstrumentKey.name.in_(without_keys)).distinct()

        if with_keys and without_keys:
            return with_query.except_(without_query)
        elif with_keys:
            return with_query
        elif without_keys:
            return query.except_(without_query)
        return query.distinct()

    @staticmethod
    def query_pitches(with_pitches = [ ], without_pitches = [ ]):
        '''Query events with and without pitches:

        ::

            >>> with_pitches = [ ]
            >>> without_pitches = [ ]
            >>> query = Event.query_pitches(with_pitches=with_pitches, without_pitches=without_pitches)

        Returns SQLAlchemy Query instance.
        '''
        from sasha.core.domain import Partial

        with_pitches = [float(pitchtools.NamedPitch(x)) for x in with_pitches]
        without_pitches = [float(pitchtools.NamedPitch(x)) for x in without_pitches]

        query = SASHA.get_session().query(Event).\
            join(Partial)

        with_query = None
        if with_pitches:
            to_intersect = [query.filter(Partial.pitch_number.in_([x])) for x in with_pitches]
            with_query = query.intersect(*to_intersect).distinct()

        without_query = None
        if without_pitches:
            without_query = query.filter(Partial.pitch_number.in_(without_pitches)).distinct()

        if with_pitches and without_pitches:
            return with_query.except_(without_query)
        elif with_pitches:
            return with_query
        elif without_pitches:
            return query.except_(without_query)
        return query.distinct()

    @staticmethod
    def query_pitch_classes(with_pcs = [ ], without_pcs = [ ]):
        '''Query events with and without pitch classes:

        ::

            >>> with_pcs = [ ]
            >>> without_pcs = [ ]
            >>> query = Event.query_pitch_classes(with_pcs=with_pcs, without_pcs=without_pcs)

        Returns SQLAlchemy Query instance.
        '''
        from sasha.core.domain import Partial

        with_pcs = [float(pitchtools.NamedPitchClass(x)) for x in with_pcs]
        without_pcs = [float(pitchtools.NamedPitchClass(x)) for x in without_pcs]

        query = SASHA.get_session().query(Event).\
            join(Partial)

        with_query = None
        if with_pcs:
            to_intersect = [query.filter(Partial.pitch_class_number.in_([x])) for x in with_pcs]
            with_query = query.intersect(*to_intersect).distinct()

        without_query = None
        if without_pcs:
            without_query = query.filter(Partial.pitch_class_number.in_(without_pcs)).distinct()

        if with_pcs and without_pcs:
            return with_query.except_(without_query)
        elif with_pcs:
            return with_query
        elif without_pcs:
            return query.except_(without_query)
        return query
