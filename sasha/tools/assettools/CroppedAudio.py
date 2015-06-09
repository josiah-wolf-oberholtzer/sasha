import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.wrappertools import Playback
from sasha.tools.assettools.SourceAudio import SourceAudio
from scikits import audiolab


class CroppedAudio(Asset):

    __requires__ = SourceAudio

    file_suffix = 'aif'
    media_type = 'source_audio'
    plugin_label = 'cropped'

    ### PUBLIC METHODS ###

    def playback(self):
        Playback()(self.path)

    def write(self, **kwargs):
        samples, samplerate = SourceAudio(self).read()
        start = int(len(samples) * 0.2)
        stop = int(len(samples) * 0.9)
        cropped_samples = samples[start:stop]
        snd = audiolab.Sndfile(self.path, 'w', audiolab.Format('aiff'), 1, samplerate)
        snd.write_frames(cropped_samples)
        snd.close()
