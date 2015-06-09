from sasha.tools.wrappertools import FFTExtract
from sasha.plugins.audio import CroppedAudio
from sasha.plugins.analysis.FFTExtractPlugin import FFTExtractPlugin


class ConstantQAnalysis(FFTExtractPlugin):

    file_suffix = 'constant_q'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_constant_q(audio_filename, analysis_filename)
