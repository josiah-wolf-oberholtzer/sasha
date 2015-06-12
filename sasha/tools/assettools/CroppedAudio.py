from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.SourceAudio import SourceAudio
from sasha.tools.wrappertools import Playback


class CroppedAudio(Asset):

    ### CLASS VARIABLES ###

    __requires__ = SourceAudio
    __slots__ = ()
    file_suffix = 'aif'
    media_type = 'source_audio'
    plugin_label = 'cropped'

    ### PUBLIC METHODS ###

    def playback(self):
        Playback()(self.path)

    def write(self, **kwargs):
        from scikits import audiolab
        samples, samplerate = SourceAudio(self).read()
        start = int(len(samples) * 0.2)
        stop = int(len(samples) * 0.9)
        cropped_samples = samples[start:stop]
        snd = audiolab.Sndfile(
            self.path,
            'w',
            audiolab.Format('aiff'),
            1,
            samplerate,
            )
        snd.write_frames(cropped_samples)
        snd.close()