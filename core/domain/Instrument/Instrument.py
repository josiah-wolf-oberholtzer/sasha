from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint

from sasha import SASHA
from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class Instrument(_Base, _DomainObject):

    __fixture_paths__ = (
        'description',
        'name',
        'parent.name',
    )

    ### SQLALCHEMY ###

    __table_args__ = (UniqueConstraint('id', 'name', 'parent_id'), { })

    description = Column(String)
    name = Column(String, unique=True)
    parent_id = Column(Integer, ForeignKey('instruments.id'), nullable=True)
    @declared_attr
    def children(cls):
        return relationship('Instrument', backref=backref('parent', remote_side=lambda: cls.id))

    ### PUBLIC METHODS ###

    @classmethod
    def with_events(cls):
        from sasha.core.domain.Event import Event
        return SASHA.get_session( ).query(cls).join(Event).distinct( ).all( )
