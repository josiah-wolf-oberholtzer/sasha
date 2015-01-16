import numpy
from sasha.tools.analysistools import Frame


def test_Frame___init___01():

    f = Frame(numpy.array([0.1, 0.2, 0.3]), 1024, 0, 44100)
