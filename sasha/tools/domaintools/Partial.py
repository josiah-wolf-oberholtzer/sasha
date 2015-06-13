from abjad.tools import pitchtools

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from sasha.tools.domaintools.DomainObject import DomainObject


class Partial(DomainObject):

    ### SQLALCHEMY ###

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref='partials')
    pitch_number = Column(Float)
    pitch_class_number = Column(Float)
    octave_number = Column(Integer)
    amplitude = Column(Float)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{}({!r}, {})>'.format(
            type(self).__name__,
            pitchtools.NamedPitch(self.pitch_number).pitch_name,
            self.amplitude,
            )