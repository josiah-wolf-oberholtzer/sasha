from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sasha.core.domain.DomainObject import DomainObject


class InstrumentModel(DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='instrument_models')
    name = Column(String)

