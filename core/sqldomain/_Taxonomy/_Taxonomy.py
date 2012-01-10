from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import backref, relationship


class _Taxonomy(object):

    __tablename__ = 'taxonomies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    kind = Column(String)
    hierarchical = Column(Boolean)

    @declared_attr
    def parent_id(cls):
        return Column(Integer, ForeignKey('taxonomies.id'), nullable=True)

    @declared_attr
    def children(cls):
        return relationship(str(cls.__name__), backref=backref('parent', remote_side=lambda: cls.id))
    
_Taxonomy = declarative_base(cls=_Taxonomy)
