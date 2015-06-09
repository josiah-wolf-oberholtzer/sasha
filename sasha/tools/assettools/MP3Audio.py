import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.SourceAudio import SourceAudio
from sasha.tools.wrappertools import LAME
from sasha.tools.wrappertools import Playback


class MP3Audio(Asset):

    __requires__ = SourceAudio

    media_type = 'mp3s'
    file_suffix = 'mp3'

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def playback(self):
        Playback()(self.path)

    def write(self, **kwargs):
        LAME()(SourceAudio(self).path, self.path)