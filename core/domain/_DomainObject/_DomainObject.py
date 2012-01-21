from ConfigParser import ConfigParser
import os

from abjad.tools.iotools import uppercamelcase_to_underscore_delimited_lowercase
from abjad.tools.iotools import underscore_delimited_lowercase_to_uppercamelcase
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

    ### PUBLIC ATTRIBUTES ###

    @property
    def canonical_name(self):
        cls_name = uppercamelcase_to_underscore_delimited_lowercase(type(self).__name__)
        if hasattr(self, 'name'):
            return '%s__%s' % (cls_name, str(self.name))
        return '%s__%s' % (cls_name, self.id)

    ### PUBLIC METHODS ###

    @classmethod
    def from_canonical_name_prefix(cls, name):
        parts = name.split('__')
        cls_name = underscore_delimited_lowercase_to_uppercamelcase(parts[0])
        if cls_name != cls.__name__:
            return None
        if not parts[1].isdigit( ):
            return cls.get(name=parts[1])
        return cls.get(id=int(parts[1]))

    def write_fixture(self):
        config = ConfigParser( )
        config.add_section('main')
        for path in self.__fixture_paths__:
            path = path.split('.')
            result = getattr(self, path[0])
            for subpath in path[1:]:
                if isinstance(result, (tuple, list)):
                    result = [getattr(x, subpath) for x in result]
                elif isinstance(result, type(None)):
                    result = ''
                    break
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

    @classmethod
    def get_one(cls, **kwargs):
        if kwargs:
            return SASHACFG.get_session( ).query(cls).filter_by(**kwargs).one( )
        return SASHACFG.get_session( ).query(cls).one( )
