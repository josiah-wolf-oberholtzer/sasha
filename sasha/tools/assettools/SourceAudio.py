import hashlib
import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.wrappertools import Playback


class SourceAudio(Asset):

    ### CLASS VARIABLES ###

    media_type = 'source_audio'
    file_suffix = ''

    ### PUBLIC METHODS ###

    def playback(self):
        Playback()(self.path)

    def read(self):
        from scikits import audiolab
        snd = audiolab.Sndfile(self.path, 'r')
        samplerate = snd.samplerate
        samples = snd.read_frames(snd.nframes)
        snd.close()
        self._asset = (samples, samplerate)
        return samples, samplerate

    ### PUBLIC PROPERTIES ###

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
        from sasha import sasha_configuration
        media_path = sasha_configuration.get_media_path(self.media_type)
        asset_path = os.path.join(media_path, self.client.name)
        return asset_path