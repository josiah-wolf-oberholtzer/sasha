from sqlalchemy import Column, Date, ForeignKey, Integer, String
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
