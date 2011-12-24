import hashlib
import os
from sasha import SASHACFG
from sasha.core.plugins import _MediaPlugin
from sasha.core.wrappers import Playback
from scikits.audiolab import Sndfile


class SourceAudio(_MediaPlugin):

    _media = 'source_audio'
    _suffix = ''

    ### PUBLIC ATTRIBUTES ###

    @property
    def duration_ms(self):
        samples, samplerate = self.read( )
        return (len(samples) / float(samplerate)) * 1000.

    @property
    def md5(self):
        f = open(self.path, 'r')
        hash = hashlib.new('md5')
        hash.update(f.read( ))
        f.close( )
        return hash.hexdigest( )

    ### PUBLIC METHODS ###

    def playback(self):
        Playback( )(self.path)

    def read(self):
        snd = Sndfile(self.path, 'r')
        samplerate = snd.samplerate
        samples = snd.read_frames(snd.nframes)
        snd.close( )
        object.__setattr__(self, '_asset', (samples, samplerate))
        return samples, samplerate

    
