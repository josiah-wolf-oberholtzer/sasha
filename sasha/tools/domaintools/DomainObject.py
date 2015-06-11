from ConfigParser import ConfigParser
import os
from abjad.tools import stringtools
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base


class DomainObject(object):

    ### CLASS VARIABLES ###

    __fixture_paths__ = ()

    ### SQLALCHEMY ###

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return stringtools.to_snake_case(cls.__name__) + 's'

    ### SPECIAL METHODS ###

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s(%r)>' % (type(self).__name__, self.name)
        return '<%s()>' % type(self).__name__

    ### PUBLIC METHODS ###

    @classmethod
    def from_canonical_name_prefix(cls, name):
        parts = name.split('__')
        cls_name = stringtools.underscore_delimited_lowercase_to_uppercamelcase(parts[0])
        if cls_name != cls.__name__:
            return None
        if not parts[1].isdigit():
            return cls.get(name=parts[1])
        return cls.get(id=int(parts[1]))

    @classmethod
    def get(cls, **kwargs):
        from sasha import sasha_configuration
        session = sasha_configuration.get_session()
        if kwargs:
            objects = session.query(cls).filter_by(**kwargs).all()
        else:
            objects = session.query(cls).all()
        #session.close()
        return objects

    @classmethod
    def get_fixtures(cls):
        from sasha import sasha_configuration
        from sasha.tools.systemtools import Fixture
        fixtures_path = os.path.join(sasha_configuration.get_media_path('fixtures'), cls.__tablename__)
        cls_name = stringtools.to_snake_case(cls.__name__)
        fixture_files = filter(lambda x: x.startswith(cls_name) and x.endswith('.ini'),
            os.listdir(fixtures_path))
        return [Fixture(os.path.join(fixtures_path, x)) for x in fixture_files]

    @classmethod
    def get_one(cls, **kwargs):
        from sasha import sasha_configuration
        session = sasha_configuration.get_session()
        if kwargs:
            objects = session.query(cls).filter_by(**kwargs).one()
        else:
            objects = session.query(cls).one()
        #session.close()
        return objects

    def write_fixture(self):
        from sasha import sasha_configuration
        config = ConfigParser()
        config.add_section('main')
        config.set('main', '__cls__', type(self).__name__)
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
        directory = os.path.join(sasha_configuration.get_media_path('fixtures'), self.__tablename__)
        if not os.path.exists(directory):
            os.mkdir(directory)
        fixture_path = os.path.join(directory,
            stringtools.to_snake_case(type(self).__name__) + '__' +
            stringtools.string_to_strict_directory_name(str(self.name)) + '.ini')
        f = open(fixture_path, 'w')
        config.write(f)
        f.close()

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        cls_name = stringtools.to_snake_case(type(self).__name__)
        if hasattr(self, 'name'):
            return '%s__%s' % (cls_name, str(self.name))
        return '%s__%s' % (cls_name, self.id)

DomainObject = declarative_base(cls=DomainObject)