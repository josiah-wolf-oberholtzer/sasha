from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from sasha.core.sqldomain._DomainObject import _DomainObject


class Event(_DomainObject):

    description = Column(String)

    filename = Column(String)

    fingering_id = Column(Integer, ForeignKey('fingerings.id'))
    fingering = relationship('Fingering', backref='events')

    hash = Column(String)

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='events')

    instrument_model_id = Column(Integer, ForeignKey('instrument_models.id'))
    instrument_model = relationship('InstrumentModel', backref='events')

    performer_id = Column(Integer, ForeignKey('performers.id'))
    performer = relationship('Performer', backref='events')

    recording_date = Column(Date, nullable = True)

    recording_location_id = Column(Integer, ForeignKey('recording_locations.id'))
    recording_location = relationship('RecordingLocation', backref='events')
