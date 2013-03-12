from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint

from sasha import SASHA
from sasha.core.domain.DomainObject import DomainObject


class Instrument(DomainObject):

    __fixture_paths__ = (
        'description',
        'instrument_keys.name',
        'name',
        'parent.name',
        'transposition',
    )

    ### SQLALCHEMY ###

    # __table_args__ = (UniqueConstraint('id', 'name'), { })

    description = Column(String, nullable=True)
    name = Column(String, unique=True)
    parent_id = Column(Integer, ForeignKey('instruments.id'), nullable=True)
    transposition = Column(Integer)
    @declared_attr
    def children(cls):
        return relationship('Instrument', backref=backref('parent', remote_side=lambda: cls.id))

    ### PUBLIC METHODS ###

    @classmethod
    def with_events(cls):
        from sasha.core.domain.Event import Event
        return SASHA.get_session().query(cls).join(Event).distinct().all()
