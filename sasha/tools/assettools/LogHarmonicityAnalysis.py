from sasha.tools.wrappertools import FFTExtract
from sasha.tools.assettools.CroppedAudio import CroppedAudio
from sasha.tools.assettools.FFTExtractPlugin import FFTExtractPlugin


class LogHarmonicityAnalysis(FFTExtractPlugin):

    file_suffix = 'log_harmonicity'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_log_harmonicity(audio_filename, analysis_filename)