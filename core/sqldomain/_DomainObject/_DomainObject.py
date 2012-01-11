from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class _DomainObject(object):

    ### SQLALCHEMY ###

    @declared_attr
    def __tablename__(cls):
        return uppercamelcase_to_underscore_delimited_lowercase(cls.__name__) + 's'

    id = Column(Integer, primary_key=True)

_DomainObject = declarative_base(cls=_DomainObject)
