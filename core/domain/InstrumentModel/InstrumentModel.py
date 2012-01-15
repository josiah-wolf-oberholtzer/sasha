from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class InstrumentModel(_Base, _DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='instrument_models')
    name = Column(String)

