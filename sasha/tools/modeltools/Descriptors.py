import mongoengine


class Descriptors(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    spectral_centroid = mongoengine.FloatField()
    spectral_crest = mongoengine.FloatField()
    spectral_flatness = mongoengine.FloatField()
    spectral_kurtosis = mongoengine.FloatField()
    spectral_rolloff = mongoengine.FloatField()
    spectral_skewness = mongoengine.FloatField()
    spectral_spread = mongoengine.FloatField()

    ### PUBLIC METHODS ###

    @staticmethod
    def from_event(event):
        from sasha.tools import assettools
        analysis = assettools.LinearSpectrumAnalysis(event)
        spectral_centroid = analysis.calculate_spectral_centroid()
        spectral_crest = analysis.calculate_spectral_crest()
        spectral_flatness = analysis.calculate_spectral_flatness()
        spectral_kurtosis = analysis.calculate_spectral_kurtosis()
        spectral_rolloff = analysis.calculate_spectral_rolloff()
        spectral_skewness = analysis.calculate_spectral_skewness()
        spectral_spread = analysis.calculate_spectral_spread()
        descriptors = Descriptors(
            spectral_centroid=spectral_centroid,
            spectral_crest=spectral_crest,
            spectral_flatness=spectral_flatness,
            spectral_kurtosis=spectral_kurtosis,
            spectral_rolloff=spectral_rolloff,
            spectral_skewness=spectral_skewness,
            spectral_spread=spectral_spread,
            )
        return descriptors