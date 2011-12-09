from sasha.core.wrappers import FFTExtract
from sasha.plugins.audio import SourceAudio
from sasha.plugins.analysis._FFTExtractPlugin import _FFTExtractPlugin


class ChromaAnalysis(_FFTExtractPlugin):

    _suffix = 'chroma'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete( )
        audio_filename = SourceAudio(self).path
        analysis_filename = self.path
        FFTExtract( ).write_chroma(audio_filename, analysis_filename)
