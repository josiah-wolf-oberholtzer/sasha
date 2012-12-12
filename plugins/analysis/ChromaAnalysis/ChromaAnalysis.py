from sasha.core.wrappers import FFTExtract
from sasha.plugins.audio import CroppedAudio
from sasha.plugins.analysis.FFTExtractPlugin import FFTExtractPlugin


class ChromaAnalysis(FFTExtractPlugin):

    file_suffix = 'chroma'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_chroma(audio_filename, analysis_filename)
