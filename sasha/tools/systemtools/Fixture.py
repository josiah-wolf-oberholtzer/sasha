import os
from ConfigParser import ConfigParser


class Fixture(dict):

    ### INITIALIZER ###

    def __init__(self, path):
        assert os.path.exists(path)
        config = ConfigParser()
        with open(path, 'r') as file_pointer:
            config.readfp(file_pointer)
        for section in config.sections():
            self[section] = {}
            for option, value in config.items(section):
                self[section][option] = value