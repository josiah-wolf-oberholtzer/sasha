import os
from sasha.core.plugins import _MediaPlugin
from sasha.core.wrappers import LAME
from sasha.core.wrappers import Playback
from sasha.plugins.audio.SourceAudio import SourceAudio


class MP3Audio(_MediaPlugin):

    _media = 'mp3s'
    _requires = (SourceAudio,)
    _suffix = 'mp3'

    ### PUBLIC METHODS ###

    def playback(self):
        Playback( )(self.path)

    def write(self, **kwargs):
        LAME( )(SourceAudio(self).path, self.path)
