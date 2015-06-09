import abc
import os
from numpy import mean
from numpy import std
from sasha.tools.assettools.Asset import Asset
from sasha.tools.wrappertools import FFTExtract
from sasha.tools.assettools import CroppedAudio


class FFTExtractPlugin(Asset):

    __requires__ = CroppedAudio
    __slots__ = ('_asset', '_client', '_mean', '_std')

    media_type = 'analyses'

    def __init__(self, arg):
        Asset.__init__(self, arg)
        object.__setattr__(self, '_mean', None)
        object.__setattr__(self, '_std', None)

    ### PUBLIC ATTRIBUTES ###

    @property
    def mean(self):
        return self._mean

    @property
    def std(self):
        return self._std

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def read(self):
        if os.path.exists(self.path):
            result = FFTExtract().read_analysis(self.path)
            object.__setattr__(self, '_asset', result)
            object.__setattr__(self, '_mean', mean(self.asset, axis=0))
            object.__setattr__(self, '_std', std(self.asset, axis=0))
            return result
        else:
            raise Exception('Path "%s" does not exist' % self.path)

    @abc.abstractmethod
    def write(self, **kwargs):
        raise NotImplemented
