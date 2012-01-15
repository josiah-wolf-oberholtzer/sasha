from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint

from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class Fingering(_Base, _DomainObject):

    ### SQLALCHEMY ###

    __table_args__ = (UniqueConstraint('id', 'instrument_id', 'compact_representation'), { })

    compact_representation = Column(String)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    instrument = relationship('Instrument', backref='fingerings')

    @declared_attr
    def instrument_keys(cls):
        association_table = Table('fingering_key_associations',
            cls.metadata,
            Column('fingering_id', Integer, ForeignKey('fingerings.id')),
            Column('instrument_key_id', Integer, ForeignKey('instrument_keys.id')))
        return relationship('InstrumentKey',
            secondary=association_table, backref='fingerings')

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%r, %s)>' % (type(self).__name__, str(self.instrument.name),
            [str(x.name) for x in self.instrument_keys])

    ### PRIVATE METHODS ###

    def _generate_compact_representation(self):
        repr = ''
        for key in sorted(self.instrument.instrument_keys, key=lambda x: x.name):
            if key in self.instrument_keys:
                repr += '1'
            else:
                repr += '0'
        return repr
