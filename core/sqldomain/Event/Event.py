from sqlalchemy import and_, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

from sasha import SASHACFG
from sasha.core.sqldomain._Base import _Base
from sasha.core.sqldomain._DomainObject import _DomainObject
from sasha.core.wrappers import AudioDB


class Event(_Base, _DomainObject):

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

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%r, %s)>' % (type(self).__name__, str(self.name),
            [str(x.name) for x in self.fingering.instrument_keys])

    ### PUBLIC ATTRIBUTES ###

    @property
    def source_audio(self):
        from sasha.plugins.audio import SourceAudio
        return SourceAudio(self)

    ### PUBLIC METHODS ###

    def query_audiodb(self, method, limit = 10):
        from sasha.core.wrappers import AudioDB
        assert isinstance(limit, int) and 0 < limit
        if method in SASHACFG['audioDB']:
            adb = AudioDB(method)
            return adb.query(self, limit)
        else:
            raise ValueError('Unknown search method "%s".' % repr(method))

    @staticmethod
    def query_keys(instrument_name, with_keys = [ ], without_keys = [ ]):
        from sasha.core.sqldomain import Fingering, Instrument, InstrumentKey
        instrument = Instrument.get(name=instrument_name)[0]
        query = SASHACFG.get_session( ).query(Event).\
            filter_by(instrument=instrument).\
            join('fingering', 'instrument_keys').\
            join(Instrument)

        to_intersect = [query.filter(InstrumentKey.name.in_([key])) for key in with_keys]
        with_query = query.intersect(*to_intersect).distinct( )

        without_query = query.filter(InstrumentKey.name.in_(without_keys)).distinct( )

        if with_keys and without_keys:
            return with_query.except_(without_query)
        elif with_keys:
            return with_query
        return query.except_(without_query)
