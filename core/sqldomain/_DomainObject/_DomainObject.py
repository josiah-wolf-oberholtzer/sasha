from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from sqlalchemy.ext.declarative import declared_attr


class _DomainObject(object):

    ### SQLALCHEMY ###

    @declared_attr
    def __tablename__(cls):
        return uppercamelcase_to_underscore_delimited_lowercase(cls.__name__) + 's'
