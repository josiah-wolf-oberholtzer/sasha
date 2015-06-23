import os
import json


class Fixture(dict):

    ### INITIALIZER ###

    def __init__(self, path):
        assert os.path.exists(path)
        with open(path, 'r') as file_pointer:
            self.update(json.load(file_pointer))