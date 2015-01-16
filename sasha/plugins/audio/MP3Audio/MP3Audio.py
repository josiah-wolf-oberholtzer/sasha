import os
from sasha.core.plugins._MediaPlugin import _MediaPlugin
from sasha.core.wrappers import LAME
from sasha.core.wrappers import Playback
from sasha.plugins.audio.SourceAudio import SourceAudio


class MP3Audio(_MediaPlugin):

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
