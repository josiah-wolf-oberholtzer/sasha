from abc import ABCMeta, abstractmethod
from ConfigParser import ConfigParser
import os

from abjad.tools import stringtools
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

from sasha import SASHA


class DomainObject(object):

    ### CLASS ATTRIBUTES ###

    __fixture_paths__ = ()

    ### SQLALCHEMY ###

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return stringtools.uppercamelcase_to_underscore_delimited_lowercase(cls.__name__) + 's'

    ### OVERRIDES ###

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s(%r)>' % (type(self).__name__, self.name)
        return '<%s()>' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def canonical_name(self):
        cls_name = stringtools.uppercamelcase_to_underscore_delimited_lowercase(type(self).__name__)
        if hasattr(self, 'name'):
            return '%s__%s' % (cls_name, str(self.name))
        return '%s__%s' % (cls_name, self.id)

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
        session = SASHA.get_session()
        if kwargs:
            objects = session.query(cls).filter_by(**kwargs).all()
        else:
            objects = session.query(cls).all()
        #session.close()
        return objects

    @classmethod
    def get_fixtures(cls):
        from sasha.core.bootstrap import Fixture
        fixtures_path = os.path.join(SASHA.get_media_path('fixtures'), cls.__tablename__)
        cls_name = stringtools.uppercamelcase_to_underscore_delimited_lowercase(cls.__name__)
        fixture_files = filter(lambda x: x.startswith(cls_name) and x.endswith('.ini'),
            os.listdir(fixtures_path))
        return [Fixture(os.path.join(fixtures_path, x)) for x in fixture_files]

    @classmethod
    def get_one(cls, **kwargs):
        session = SASHA.get_session()
        if kwargs:
            objects = session.query(cls).filter_by(**kwargs).one()
        else:
            objects = session.query(cls).one()
        #session.close()
        return objects

    def write_fixture(self):
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
        directory = os.path.join(SASHA.get_media_path('fixtures'), self.__tablename__)
        if not os.path.exists(directory):
            os.mkdir(directory)
        fixture_path = os.path.join(directory,
            stringtools.uppercamelcase_to_underscore_delimited_lowercase(type(self).__name__) + '__' +
            stringtools.string_to_strict_directory_name(str(self.name)) + '.ini')
        f = open(fixture_path, 'w')
        config.write(f)
        f.close()

DomainObject = declarative_base(cls=DomainObject)


