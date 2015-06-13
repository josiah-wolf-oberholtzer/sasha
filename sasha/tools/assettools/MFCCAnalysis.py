from sasha.tools.executabletools import FFTExtract
from sasha.tools.assettools.CroppedAudio import CroppedAudio
from sasha.tools.assettools.FFTExtractPlugin import FFTExtractPlugin


class MFCCAnalysis(FFTExtractPlugin):

    ### CLASS VARIABLES ###

    __slots__ = ()
    file_suffix = 'mfcc'

    ### PUBLIC METHODS ###

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_mfcc(audio_filename, analysis_filename)