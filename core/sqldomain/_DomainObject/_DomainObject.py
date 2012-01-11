from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from sqlalchemy.ext.declarative import declared_attr

from sasha import SASHACFG


class _DomainObject(object):

    ### SQLALCHEMY ###

    @declared_attr
    def __tablename__(cls):
        return uppercamelcase_to_underscore_delimited_lowercase(cls.__name__) + 's'

    ### OVERRIDES ###

    def __repr__(self):
        if hasattr(self, 'name'):
            return '%s(%r)' % (type(self).__name__, self.name)
        return '%s()' % type(self).__name__

    ### PUBLIC METHODS ###

    @classmethod
    def get(cls, **kwargs):
        if kwargs:
            return SASHACFG.get_session( ).query(cls).filter_by(**kwargs).all( )
        return SASHACFG.get_session( ).query(cls).all( )
