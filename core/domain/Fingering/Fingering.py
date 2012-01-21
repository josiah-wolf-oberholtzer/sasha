from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from abjad.tools.iotools import underscore_delimited_lowercase_to_uppercamelcase
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint

from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class Fingering(_Base, _DomainObject):

    ### SQLALCHEMY ###

    __table_args__ = (
        UniqueConstraint('id', 'instrument_id', 'compact_representation'),
        { })

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

    ### PUBLIC ATTRIBUTES ###

    @property
    def canonical_name(self):
        cls_name = uppercamelcase_to_underscore_delimited_lowercase(type(self).__name__)
        instrument_name = '_'.join(self.instrument.name.lower( ).split( ))
        return '%s__%s__%s' % (cls_name, instrument_name, self.compact_representation)

    ### PRIVATE METHODS ###

    def _generate_compact_representation(self):
        repr = ''
        for key in sorted(self.instrument.instrument_keys, key=lambda x: x.name):
            if key in self.instrument_keys:
                repr += '1'
            else:
                repr += '0'
        return repr

    ### PUBLIC METHODS ###

    @classmethod
    def from_canonical_name_prefix(cls, name):
        from sasha import Instrument
        parts = name.split('__')
        cls_name = underscore_delimited_lowercase_to_uppercamelcase(parts[0])
        if cls_name != cls.__name__:
            return None
        instrument_name = ' '.join(parts[1].split('_')).title( )
        instrument = Instrument.get(name=instrument_name)[0]
        compact_representation = parts[2]
        return cls.get(instrument=instrument, compact_representation=compact_representation)[0]
        
