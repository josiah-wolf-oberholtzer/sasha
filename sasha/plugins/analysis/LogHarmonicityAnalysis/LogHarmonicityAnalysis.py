from sasha.core.wrappers import FFTExtract
from sasha.plugins.audio import CroppedAudio
from sasha.plugins.analysis.FFTExtractPlugin import FFTExtractPlugin


class LogHarmonicityAnalysis(FFTExtractPlugin):

    file_suffix = 'log_harmonicity'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_log_harmonicity(audio_filename, analysis_filename)
