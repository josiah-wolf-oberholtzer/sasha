import os
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import models
import unittest


class LinearSpectrumAnalysisTests(unittest.TestCase):

    def setUp(self):
        sasha_configuration.environment = 'testing'

    def tearDown(self):
        pass

    def test___init__(self):
        event_a = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        event_b = models.Event.objects.get(
            name='event__alto_saxophone__br_123.aif')
        analysis_a = assettools.LinearSpectrumAnalysis(event_a)
        analysis_b = assettools.LinearSpectrumAnalysis(event_b)
        self.assertEqual(
            analysis_a.path,
            os.path.join(
                sasha_configuration.get_media_path('analyses'),
                'event__{}.linear_spectrum'.format(event_a.md5),
                ),
            )
        self.assertEqual(
            analysis_b.path,
            os.path.join(
                sasha_configuration.get_media_path('analyses'),
                'event__{}.linear_spectrum'.format(event_b.md5),
                ),
            )

    def test_write(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        analysis.delete()
        self.assertFalse(analysis.exists)
        analysis.write()
        self.assertTrue(analysis.exists)

    def test_calculate_spectral_centroid(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_centroid()
        self.assertAlmostEqual(result, 783.7433598705129)

    def test_calculate_spectral_crest(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_crest()
        self.assertAlmostEqual(result, 0.075993532431403346)

    def test_calculate_spectral_flatness(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_flatness()
        self.assertAlmostEqual(result, 4.247625609963788e-05)

    def test_calculate_spectral_kurtosis(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_kurtosis()
        self.assertAlmostEqual(result, 1389.031871906816)

    def test_calculate_spectral_skewness(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_skewness()
        self.assertAlmostEqual(result, 34.80170954439035)

    def test_calculate_spectral_spread(self):
        event = models.Event.objects.get(
            name='event__alto_saxophone__br_042.aif')
        analysis = assettools.LinearSpectrumAnalysis(event)
        result = analysis.calculate_spectral_spread()
        self.assertAlmostEqual(result, 429.27266978906056)