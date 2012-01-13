from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import ForeignKeyConstraint

from sasha.core.sqldomain._Base import _Base
from sasha.core.sqldomain._DomainObject import _DomainObject


class Fingering(_Base, _DomainObject):

    ### SQLALCHEMY ###

    instrument_id = Column(Integer, ForeignKey('instruments.id'))
    instrument = relationship('Instrument', backref='fingerings')

    @declared_attr
    def instrument_keys(cls):
        association_table = Table('fingering_key_associations',
            cls.metadata,
            Column('fingering_id', Integer, ForeignKey('fingerings.id')),
            Column('instrument_key_id', Integer, ForeignKey('instrument_keys.id')))
#            ForeignKeyConstraint(['fingering_id', 'instrument_key_id'], ['fingerings.id', 'instrument_keys.id']))
        return relationship('InstrumentKey',
            secondary=association_table, backref='fingerings')

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%r, %s)>' % (type(self).__name__, str(self.instrument.name),
            [str(x.name) for x in self.instrument_keys])
