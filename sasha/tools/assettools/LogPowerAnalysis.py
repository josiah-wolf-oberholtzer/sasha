from sasha.tools.executabletools import FFTExtract
from sasha.tools.assettools.CroppedAudio import CroppedAudio
from sasha.tools.assettools.FFTExtractPlugin import FFTExtractPlugin


class LogPowerAnalysis(FFTExtractPlugin):

    ### CLASS VARIABLES ###

    __slots__ = ()
    file_suffix = 'log_power'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_log_power(audio_filename, analysis_filename)