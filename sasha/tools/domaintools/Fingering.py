from abjad.tools import stringtools
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint
from sasha.tools.domaintools.DomainObject import DomainObject
from webhelpers.html import HTML


class Fingering(DomainObject):

    ### SQLALCHEMY ###

    __table_args__ = (
        UniqueConstraint('id', 'instrument_id', 'compact_representation'),
        {})

    compact_representation = Column(String)
    instrument_id = Column(
        Integer,
        ForeignKey('instruments.id'),
        nullable=False,
        )
    instrument = relationship('Instrument', backref='fingerings')

    @declared_attr
    def instrument_keys(cls):
        association_table = Table(
            'fingering_key_associations',
            cls.metadata,
            Column(
                'fingering_id',
                Integer,
                ForeignKey('fingerings.id'),
                ),
            Column(
                'instrument_key_id',
                Integer,
                ForeignKey('instrument_keys.id'),
                ),
            )
        return relationship(
            'InstrumentKey',
            secondary=association_table,
            backref='fingerings',
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        from sasha import Instrument
        instrument = Instrument.get_one(id=self.instrument_id)
        return '<{}({!r}, {!r})>'.format(
            type(self).__name__,
            str(instrument.name),
            self.compact_representation,
            )

    ### PRIVATE METHODS ###

    def _generate_compact_representation(self):
        result = ''
        for key in sorted(
            self.instrument.instrument_keys,
            key=lambda x: x.name,
            ):
            if key in self.instrument_keys:
                result += '1'
            else:
                result += '0'
        return result

    ### PUBLIC METHODS ###

    def find_similar_fingerings(self, n=10):
        def compare(a, b):
            return sum(1 for x, y in zip(a, b) if x == y)
        results = []
        fingerings = Fingering.get(instrument_id=self.instrument_id)
        fingerings = (x for x in fingerings if x.id != self.id)
        for fingering in fingerings:
            comparison = compare(
                self.compact_representation,
                fingering.compact_representation,
                )
            results.append((comparison, fingering))
        results.sort(key=lambda x: x[0], reverse=True)
        results = [x[1] for x in results][:n]
        return results

    def get_url(self, request):
        from sasha.tools import domaintools
        instrument = domaintools.Instrument.get_one(id=self.instrument_id)
        instrument_name = stringtools.to_dash_case(instrument.name)
        compact_representation = self.compact_representation
        return request.route_url(
            'fingering',
            instrument_name=instrument_name,
            compact_representation=compact_representation,
            )

    def get_link(self, request):
        fingering = type(self).get_one(id=self.id)
        name = ' '.join([key.name for key in fingering.instrument_keys])
        href = self.get_url(request)
        text = name
        return HTML.tag('a', href=href, c=text)

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return ' '.join([key.name for key in self.instrument_keys])