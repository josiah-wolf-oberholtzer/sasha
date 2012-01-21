from sasha.core.wrappers import FFTExtract
from sasha.plugins.audio import SourceAudio
from sasha.plugins.analysis._FFTExtractPlugin import _FFTExtractPlugin


class LinearSpectrumAnalysis(_FFTExtractPlugin):

    file_suffix = 'linear_spectrum'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete( )
        audio_filename = SourceAudio(self).path
        analysis_filename = self.path
        FFTExtract( ).write_linear_spectrum(audio_filename, analysis_filename)
