from sasha.tools import wrappertools
from sasha.tools.assettools.FFTExtractPlugin import FFTExtractPlugin


class ConstantQAnalysis(FFTExtractPlugin):

    file_suffix = 'constant_q'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        from sasha.tools import assettools
        self.delete()
        audio_filename = assettools.CroppedAudio(self).path
        analysis_filename = self.path
        wrappertools.FFTExtract().write_constant_q(
            audio_filename,
            analysis_filename,
            )