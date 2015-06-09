import inspect
import logging
import os
from ConfigParser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sasha.tools.systemtools import ImmutableDictionary


class SashaConfiguration(ImmutableDictionary):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_environment',
        '_logger',
        )

    ### INITIALIZER ###

    def __init__(self, environment='development'):
        import sasha
        sasha_root = sasha.__path__[0]
        parser = ConfigParser(dict_type=dict)
        sasha_cfg_file_path = os.path.join(sasha_root, 'sasha.cfg')
        assert os.path.exists(sasha_cfg_file_path)
        parser.read(sasha_cfg_file_path)
        assert environment in ('testing', 'development', 'deployment')
        self._environment = environment
        for section in parser.sections():
            dict.__setitem__(self, section, ImmutableDictionary())
            for option, value in parser.items(section):
                dict.__setitem__(self[section], option, value)
        self._logger = logging.getLogger('sasha')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(sasha_root, self['logging']['logfile']))
        handler.setLevel(logging.DEBUG)
        log_message = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        formatter = logging.Formatter(log_message)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    ### PUBLIC METHODS ###

    def bootstrap(self):
        from sasha.tools.systemtools import Bootstrap
        Bootstrap()()

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
        from sasha.core import domain
        from sasha.tools.domaintools.DomainObject import DomainObject
        klasses = set()
        for x in dir(domain):
            klass = getattr(domain, x)
            if hasattr(klass, '__bases__') and \
                DomainObject in inspect.getmro(klass) and \
                klass.__module__.startswith('sasha'):
                klasses.add(klass)
        return tuple(klasses)

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
        dbpath = os.path.join(self.get_media_path('databases'),
            self['sqlite']['sqlite'])
        engine = create_engine('sqlite:///%s' % dbpath)
        return sessionmaker(bind=engine)()

    ### PUBLIC PROPERTIES ###

    @property
    def env(self):
        return self._environment

    @env.setter
    def env(self, value):
        self.environment = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        assert value in ['testing', 'development', 'deployment']
        self._environment = value

    @property
    def logger(self):
        return self._logger
