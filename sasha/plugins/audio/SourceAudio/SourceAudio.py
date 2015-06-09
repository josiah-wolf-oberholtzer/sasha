import hashlib
import os
from sasha.core.plugins._MediaPlugin import _MediaPlugin
from sasha.tools.wrappertools import Playback
from scikits.audiolab import Sndfile


class SourceAudio(_MediaPlugin):

    media_type = 'source_audio'
    file_suffix = ''

    ### PUBLIC ATTRIBUTES ###

    @property
    def duration_ms(self):
        samples, samplerate = self.read()
        return (len(samples) / float(samplerate)) * 1000.

    @property
    def md5(self):
        f = open(self.path, 'r')
        hash = hashlib.new('md5')
        hash.update(f.read())
        f.close()
        return hash.hexdigest()

    @property
    def path(self):
        from sasha import SASHA
        return os.path.join(SASHA.get_media_path(self.media_type),
            self.client.name)

    ### PUBLIC METHODS ###

    def playback(self):
        Playback()(self.path)

    def read(self):
        snd = Sndfile(self.path, 'r')
        samplerate = snd.samplerate
        samples = snd.read_frames(snd.nframes)
        snd.close()
        object.__setattr__(self, '_asset', (samples, samplerate))
        return samples, samplerate

    