from abjad.tools import pitchtools

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from sasha.core.domain.DomainObject import DomainObject


class Partial(DomainObject):

    ### SQLALCHEMY ###

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref='partials')
    pitch_number = Column(Float)
    pitch_class_number= Column(Float)
    octave_number = Column(Integer)
    amplitude = Column(Float)

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%r, %s)>' % (type(self).__name__,
            pitchtools.NamedPitch(self.pitch_number).chromatic_pitch_name, self.amplitude)
