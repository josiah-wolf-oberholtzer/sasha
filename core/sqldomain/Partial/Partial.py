from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from sasha.core.sqldomain._DomainObject import _DomainObject


class Partial(_DomainObject):

    ### SQLALCHEMY ###

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref='partials')
    pitch_class_number= Column(Float)
    octave_number = Column(Integer)
    amplitude = Column(Float)
