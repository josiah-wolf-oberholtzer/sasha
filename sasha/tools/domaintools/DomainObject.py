from ConfigParser import ConfigParser
import json
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
            result = '<{}({!r})>'
            result = result.format(
                type(self).__name__,
                self.name,
                )
        else:
            result = '<{}()>'
            result = result.format(
                type(self).__name__,
                )
        return result

    ### PUBLIC METHODS ###

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
        cls_name = stringtools.to_snake_case(cls.__name__)
        fixtures_path = os.path.join(
            sasha_configuration.get_media_path('fixtures'),
            cls.__tablename__,
            )
        fixture_file_names = os.listdir(fixtures_path)
        fixture_file_names = (
            _ for _ in fixture_file_names
            if _.startswith(cls_name) and _.endswith('.json')
            )
        fixture_file_paths = (
            os.path.join(fixtures_path, _)
            for _ in fixture_file_names
            )
        fixtures = []
        for fixture_file_path in fixture_file_paths:
            with open(fixture_file_path, 'r') as file_pointer:
                fixture = json.load(file_pointer)
            fixtures.append(fixture)
        return fixtures

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
        directory = os.path.join(
            sasha_configuration.get_media_path('fixtures'),
            self.__tablename__,
            )
        if not os.path.exists(directory):
            os.mkdir(directory)
        prefix = stringtools.to_snake_case(type(self).__name__)
        midfix = '__'
        suffix = stringtools.string_to_strict_directory_name(str(self.name))
        extension = '.ini'
        file_name = prefix + midfix + suffix + extension
        fixture_path = os.path.join(directory, file_name)
        with open(fixture_path, 'w') as file_pointer:
            config.write(file_pointer)

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_name(self):
        cls_name = stringtools.to_snake_case(type(self).__name__)
        if hasattr(self, 'name'):
            return '{}__{}'.format(cls_name, str(self.name))
        return '{}__{}'.format(cls_name, self.id)


DomainObject = declarative_base(cls=DomainObject)