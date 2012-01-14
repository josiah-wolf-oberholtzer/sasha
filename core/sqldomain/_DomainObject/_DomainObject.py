from ConfigParser import ConfigParser
import os

from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from sqlalchemy.ext.declarative import declared_attr

from sasha import SASHACFG


class _DomainObject(object):

    __fixture_paths__ = ( )

    ### SQLALCHEMY ###

    @declared_attr
    def __tablename__(cls):
        return uppercamelcase_to_underscore_delimited_lowercase(cls.__name__) + 's'

    ### OVERRIDES ###

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s(%r)>' % (type(self).__name__, self.name)
        return '<%s()>' % type(self).__name__

    ### PUBLIC METHODS ###

    def write_fixture(self):
        config = ConfigParser( )
        config.add_section('main')
        for path in self.__fixture_paths__:
            path = path.split('.')
            result = getattr(self, path[0])
            for subpath in path[1:]:
                if isinstance(result, (tuple, list)):
                    result = [getattr(x, subpath) for x in result]
                else:
                    result = getattr(result, subpath)
            if isinstance(result, (list, tuple)):
                result = ' '.join(result)
            config.set('main', '.'.join(path), result)
        fixture_path = os.path.join(SASHACFG.get_media_path('fixtures'),
            self.__tablename__,
            self.name + '.ini')
        f = open(fixture_path, 'w')
        config.write(f)
        f.close( )

    @classmethod
    def get(cls, **kwargs):
        if kwargs:
            return SASHACFG.get_session( ).query(cls).filter_by(**kwargs).all( )
        return SASHACFG.get_session( ).query(cls).all( )
