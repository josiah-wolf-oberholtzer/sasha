import math
import numpy
from sasha.tools.executabletools import FFTExtract
from sasha.tools.assettools.CroppedAudio import CroppedAudio
from sasha.tools.assettools.FFTExtractPlugin import FFTExtractPlugin


class LinearSpectrumAnalysis(FFTExtractPlugin):

    ### CLASS VARIABLES ###

    __slots__ = ()
    file_suffix = 'linear_spectrum'

    ### PUBLIC METHODS ###

    def calculate_spectral_centroid(self):
        from sasha.tools import assettools
        _, sample_rate = assettools.SourceAudio(self).read()
        spectrum = abs(self.mean)
        bin_frequency_span = (sample_rate / 2.0) / len(spectrum)
        numerator = 0
        denominator = 0
        for bin_number, bin_value in enumerate(spectrum):
            frequency = bin_frequency_span * bin_number
            numerator += frequency * abs(bin_value)
            denominator += abs(bin_value)
        centroid = float(numerator) / denominator
        return centroid

    def calculate_spectral_crest(self):
        spectrum = abs(self.mean)
        spectral_sum = numpy.sum(spectrum)
        max_frequency_index = numpy.argmax(spectrum)
        spectral_maximum = spectrum[max_frequency_index]
        crest = spectral_maximum / spectral_sum
        return crest

    def calculate_spectral_flatness(self):
        try:
            from scipy import stats
            spectrum = abs(self.mean)
            geometric_mean = stats.mstats.gmean(spectrum)
            arithmetic_mean = spectrum.mean()
            flatness = geometric_mean / arithmetic_mean
        except ImportError:
            flatness = 0.
        return flatness

    def calculate_spectral_kurtosis(self):
        try:
            from scipy import stats
            spectrum = abs(self.mean)
            kurtosis = stats.kurtosis(spectrum)
        except ImportError:
            kurtosis = 0.
        return kurtosis

    def calculate_spectral_rolloff(self):
        from sasha.tools import assettools
        spectrum = abs(self.mean)
        _, sample_rate = assettools.SourceAudio(self).read()
        bin_frequency_span = (sample_rate / 2.0) / len(spectrum)
        spectral_sum = numpy.sum(spectrum)
        rolloff_sum = 0
        rolloff_index = 0
        for bin_number, bin_value in enumerate(spectrum):
            rolloff_sum += bin_value
            if rolloff_sum > (0.85 * spectral_sum):
                rolloff_index = bin_number
                break
        frequency = rolloff_index * bin_frequency_span
        return frequency

    def calculate_spectral_skewness(self):
        try:
            from scipy import stats
            spectrum = abs(self.mean)
            skewness = stats.skew(spectrum)
        except ImportError:
            skewness = 0.
        return skewness

    def calculate_spectral_spread(self):
        from sasha.tools import assettools
        spectrum = abs(self.mean)
        _, sample_rate = assettools.SourceAudio(self).read()
        centroid = self.calculate_spectral_centroid()
        bin_frequency_span = (sample_rate / 2.0) / len(spectrum)
        numerator = 0
        denominator = 0
        for bin_number, bin_value in enumerate(spectrum):
            bin_frequency = bin_frequency_span * bin_number
            numerator += ((bin_frequency - centroid) ** 2) * bin_value
            denominator += bin_value
        return math.sqrt((numerator * 1.0) / denominator)

    def write(self, **kwargs):
        self.delete()
        audio_filename = CroppedAudio(self).path
        analysis_filename = self.path
        FFTExtract().write_linear_spectrum(audio_filename, analysis_filename)