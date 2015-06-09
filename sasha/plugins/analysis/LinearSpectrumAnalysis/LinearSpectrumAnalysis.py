from sasha.tools.wrappertools import FFTExtract
from sasha.plugins.audio import CroppedAudio
from sasha.plugins.analysis.FFTExtractPlugin import FFTExtractPlugin


class LinearSpectrumAnalysis(FFTExtractPlugin):

    file_suffix = 'linear_spectrum'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_linear_spectrum(audio_filename, analysis_filename)
