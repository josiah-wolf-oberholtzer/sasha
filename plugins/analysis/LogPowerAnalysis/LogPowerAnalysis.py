from sasha.core.wrappers import FFTExtract
from sasha.plugins.audio import SourceAudio
from sasha.plugins.analysis._FFTExtractPlugin import _FFTExtractPlugin


class LogPowerAnalysis(_FFTExtractPlugin):

    _suffix = 'log_power'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete( )
        audio_filename = SourceAudio(self).path
        analysis_filename = self.path
        FFTExtract( ).write_log_power(audio_filename, analysis_filename)
