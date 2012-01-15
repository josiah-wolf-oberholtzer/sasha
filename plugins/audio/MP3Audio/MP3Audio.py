import os
from sasha.core.plugins import _MediaPlugin
from sasha.core.wrappers import LAME
from sasha.core.wrappers import Playback
from sasha.plugins.audio.SourceAudio import SourceAudio


class MP3Audio(_MediaPlugin):

    __requires__ = SourceAudio

    _media = 'mp3s'
    _suffix = 'mp3'

    ### PUBLIC METHODS ###

    def playback(self):
        Playback( )(self.path)

    def write(self, **kwargs):
        LAME( )(SourceAudio(self).path, self.path)
