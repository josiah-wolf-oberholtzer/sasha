from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from sasha.core.sqldomain._Base import _Base
from sasha.core.sqldomain._DomainObject import _DomainObject


class InstrumentKey(_Base, _DomainObject):

    ### SQLALCHEMY ###

    __table_args__ = (UniqueConstraint('instrument_id', 'name'), { })

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='instrument_keys')
    is_fractional = Column(Boolean)
    name = Column(String)
