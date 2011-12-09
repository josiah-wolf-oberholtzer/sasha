import os
import sqlite3
from ConfigParser import ConfigParser
from sasha import SASHAROOT
from sasha.core.mixins import _ImmutableDictionary


class SashaConfig(_ImmutableDictionary):

    __slots__ = ('_environment',)

    def __init__(self, environment = 'development'):
        parser = ConfigParser(dict_type = dict)
        sashacfg = os.path.join(SASHAROOT, 'sasha.cfg')

        assert os.path.exists(sashacfg)
        parser.read(sashacfg)

        assert environment in ['testing', 'development', 'deployment']
        self._environment = environment

        for section in parser.sections( ):
            dict.__setitem__(self, section, _ImmutableDictionary( ))
            for option, value in parser.items(section):
                dict.__setitem__(self[section], option, value)

    ### PUBLIC ATTRIBUTES ###

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
        if value != self._environment:
            from sasha.core.domain import _identity_map
            for map in _identity_map.itervalues( ):
                map.clear( )
        self._environment = value

    ### PUBLIC METHODS ###

    def get_binary(self, name):
        return self['binaries'][name]

    def get_sqlite3(self):
        path = os.path.join(
            self['media_root'][self.environment],
            self['media']['databases'],
            self['sqlite3']['sqlite3'])
        if not os.path.isabs(path):
            path = os.path.abspath(os.path.join(SASHAROOT, path))
        return sqlite3.Connection(path)

    def get_audiodb_parameters(self, name):
        from sasha.core.wrappers import AudioDB
        assert name in self['audioDB']

        item = self['audioDB'][name].split(',')
        db_path = os.path.join(
            self['media_root'][self.environment],
            self['media']['databases'],
            item[0].strip( ))
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(os.path.join(SASHAROOT, db_path))

        klass_path = item[1].strip( )
        module_name = klass_path.rpartition('.')[0]
        klass_name = klass_path.rpartition('.')[-1]
        module = __import__(module_name, globals(), locals(), [klass_name])
        klass = getattr(module, klass_name)

        return db_path, klass

    def get_media_path(self, name):
        path = os.path.join(
            self['media_root'][self.environment],
            self['media'][name])
        if not os.path.isabs(path):
            path = os.path.abspath(os.path.join(SASHAROOT, path))
        return path
