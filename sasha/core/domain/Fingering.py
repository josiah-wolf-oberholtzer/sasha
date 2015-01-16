from abjad.tools import stringtools

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint

from sasha.core.domain.DomainObject import DomainObject


class Fingering(DomainObject):

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
        from sasha import Instrument
        instrument = Instrument.get_one(id=self.instrument_id)
        return '<%s(%r, %r)>' % (type(self).__name__, str(instrument.name),
            self.compact_representation)

    ### PUBLIC ATTRIBUTES ###

    @property
    def canonical_name(self):
        from sasha import Instrument
        cls_name = stringtools.to_snake_case(type(self).__name__)
        instrument = Instrument.get_one(id=self.instrument_id)
        instrument_name = '_'.join(instrument.name.lower().split())
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
        cls_name = stringtools.underscore_delimited_lowercase_to_uppercamelcase(parts[0])
        if cls_name != cls.__name__:
            return None
        instrument_name = ' '.join(parts[1].split('_')).title()
        instrument = Instrument.get(name=instrument_name)[0]
        compact_representation = parts[2]
        return cls.get(instrument=instrument, compact_representation=compact_representation)[0]
        
    def find_similar_fingerings(self, n = 10):
        results = [ ]
        fingerings = Fingering.get(instrument_id=self.instrument_id)
        fingerings = [x for x in fingerings if x.id != self.id]

        def compare(a, b):
            return sum([1 for x, y in zip(a, b) if x == y])

        for fingering in fingerings:
            comparison = compare(self.compact_representation, fingering.compact_representation)
            results.append((comparison, fingering))

        return [x[1] for x in sorted(results, key=lambda x: x[0], reverse=True)][:n]
            
