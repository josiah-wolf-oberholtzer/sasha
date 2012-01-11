from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declared_attr

from sasha.core.sqldomain._Base import _Base
from sasha.core.sqldomain._DomainObject import _DomainObject


class Instrument(_Base, _DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
    parent_id = Column(Integer, ForeignKey('instruments.id'), nullable=True)
    @declared_attr
    def children(cls):
        return relationship('Instrument', backref=backref('parent', remote_side=lambda: cls.id))
