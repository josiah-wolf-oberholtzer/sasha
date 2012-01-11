from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sasha.core.sqldomain._DomainObject import _DomainObject


class InstrumentKey(_DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='instrument_keys')
    is_fractional = Column(Boolean)
    name = Column(String)
