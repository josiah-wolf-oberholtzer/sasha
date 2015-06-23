import inspect
import json
import logging
import mongoengine
import os
from ConfigParser import ConfigParser
from abjad.tools import stringtools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SashaConfiguration(dict):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_environment',
        '_logger',
        '_mongodb_client',
        )

    ### INITIALIZER ###

    def __init__(self, environment='development'):
        import sasha
        sasha_root = sasha.__path__[0]
        parser = ConfigParser(dict_type=dict)
        sasha_cfg_file_path = os.path.join(sasha_root, 'sasha.cfg')
        assert os.path.exists(sasha_cfg_file_path)
        parser.read(sasha_cfg_file_path)
        for section in parser.sections():
            self[section] = {}
            for option, value in parser.items(section):
                self[section][option] = value
        self._logger = logging.getLogger('sasha')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(sasha_root, self['logging']['logfile']))
        handler.setLevel(logging.DEBUG)
        log_message = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        formatter = logging.Formatter(log_message)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self._mongodb_client = None
        assert environment in ('testing', 'development', 'deployment')
        self._environment = environment

    ### PUBLIC METHODS ###

    def bootstrap(self):
        from sasha.tools.systemtools import Bootstrap
        Bootstrap()()

    def connect(self):
        if self._mongodb_client is not None:
            self._mongodb_client.disconnect()
        self._mongodb_client = mongoengine.connect(self.mongodb_database_name)

    @staticmethod
    def find_executable(executable_name):
        def is_executable(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)

        def extension_candidates(file_path):
            yield file_path
            for extension in os.environ.get('PATHEXT', '').split(os.pathsep):
                yield file_path + extension
        file_path, file_name = os.path.split(executable_name)
        if file_path:
            if is_executable(executable_name):
                return executable_name
        else:
            for path in os.environ['PATH'].split(os.pathsep):
                executable_file = os.path.join(path, executable_name)
                for candidate in extension_candidates(executable_file):
                    if is_executable(candidate):
                        return candidate
        return None

    def get_audiodb_parameters(self, name):
        import sasha
        sasha_root = sasha.__path__[0]
        assert name in self['audioDB']
        item = self['audioDB'][name].split(',')
        db_path = os.path.join(
            self['media_root'][self.environment],
            self['media']['databases'],
            item[0].strip())
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(os.path.join(sasha_root, db_path))
        klass_path = item[1].strip()
        module_name = klass_path.rpartition('.')[0]
        klass_name = klass_path.rpartition('.')[-1]
        module = __import__(module_name, globals(), locals(), [klass_name])
        klass = getattr(module, klass_name)
        return db_path, klass

    def get_binary(self, name):
        return self['binaries'][name]

    def get_domain_classes(self):
        from sasha.tools import domaintools
        klasses = set()
        for x in dir(domaintools):
            klass = getattr(domaintools, x)
            if hasattr(klass, '__bases__') and \
                domaintools.DomainObject in inspect.getmro(klass) and \
                klass.__module__.startswith('sasha'):
                klasses.add(klass)
        return tuple(klasses)

    def get_fixtures(self, cls):
        from sasha import sasha_configuration
        cls_name = stringtools.to_snake_case(cls.__name__)
        fixtures_path = os.path.join(
            sasha_configuration.get_media_path('fixtures'),
            cls_name + 's',
            #cls.__tablename__,
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

    def get_media_path(self, name):
        import sasha
        sasha_root = sasha.__path__[0]
        path = os.path.join(
            self['media_root'][self.environment],
            self['media'][name])
        if not os.path.isabs(path):
            path = os.path.abspath(os.path.join(sasha_root, path))
        return path

    def get_session(self):
        database_path = os.path.join(
            self.get_media_path('databases'),
            self['sqlite']['sqlite'],
            )
        engine = create_engine('sqlite:///{}'.format(database_path))
        return sessionmaker(bind=engine)()

    ### PUBLIC PROPERTIES ###

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        assert value in ['testing', 'development', 'deployment']
        self._environment = value
        self.connect()

    @property
    def logger(self):
        return self._logger

    @property
    def mongodb_client(self):
        return self.mongodb_client

    @property
    def mongodb_database_name(self):
        return 'sasha/{}'.format(self.environment)