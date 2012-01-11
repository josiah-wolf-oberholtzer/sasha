from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from sasha.core.sqldomain._DomainObject import _DomainObject


class Fingering(_DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='fingerings')

    @declared_attr
    def instrument_keys(cls):
        association_table = Table('fingering_key_associations',
            cls.metadata,
            Column('fingering_id', Integer, ForeignKey('fingerings.id')),
            Column('instrument_key_id', Integer, ForeignKey('instrument_keys.id')))
        return relationship('InstrumentKey', secondary=association_table, backref='fingerings')
