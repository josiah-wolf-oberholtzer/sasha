from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sasha.core.sqldomain._DomainObject import _DomainObject


class InstrumentModel(_DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='instrument_models')
    name = Column(String)
