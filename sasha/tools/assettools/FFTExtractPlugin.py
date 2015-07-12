import abc
import os
from numpy import mean
from numpy import std
from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.CroppedAudio import CroppedAudio
from sasha.tools.executabletools import FFTExtract


class FFTExtractPlugin(Asset):

    ### CLASS VARIABLES

    __requires__ = CroppedAudio
    __slots__ = (
        '_asset',
        '_client',
        '_mean',
        '_std',
        )
    media_type = 'analyses'

    ### INITIALIZER ###

    def __init__(self, arg):
        Asset.__init__(self, arg)
        self._mean = None
        self._std = None

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def read(self):
        if os.path.exists(self.path):
            result = FFTExtract().read_analysis(self.path)
            self._asset = result
            self._mean = mean(self.asset, axis=0)
            self._std = std(self.asset, axis=0)
            return result
        message = 'Path {!r} does not exist'.format(self.path)
        raise Exception(message)

    @abc.abstractmethod
    def write(self, **kwargs):
        raise NotImplemented

    ### PUBLIC PROPERTIES ###

    @property
    def mean(self):
        if self.asset is None:
            self.read()
        return self._mean

    @property
    def std(self):
        if self.asset is None:
            self.read()
        return self._std