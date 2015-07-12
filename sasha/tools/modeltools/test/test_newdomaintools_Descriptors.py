# -*- encoding: utf-8 -*-
from pyramid import testing
import sasha
import unittest


class DescriptorsTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_Descriptors_01(self):
        event = sasha.modeltools.Event.objects.get(
            md5='bae113a08990072eb1bfd9c85b8cce34')
        descriptors = sasha.Descriptors.from_event(event)
        self.assertIsNotNone(descriptors)
        self.assertTrue(0 < descriptors.spectral_centroid)
        self.assertTrue(0 < descriptors.spectral_crest)
        self.assertTrue(0 < descriptors.spectral_flatness)
        self.assertTrue(0 < descriptors.spectral_kurtosis)
        self.assertTrue(0 < descriptors.spectral_rolloff)
        self.assertTrue(0 < descriptors.spectral_skewness)
        self.assertTrue(0 < descriptors.spectral_spread)