import os
from ConfigParser import ConfigParser
from sasha.tools.systemtools.ImmutableDictionary import ImmutableDictionary


class Fixture(ImmutableDictionary):

    def __init__(self, path):

        assert os.path.exists(path)
        config = ConfigParser()

        f = open(path, 'r')
        config.readfp(f)
        f.close()

        for section in config.sections():
            dict.__setitem__(self, section, ImmutableDictionary())
            for option, value in config.items(section):
                dict.__setitem__(self[section], option, value)