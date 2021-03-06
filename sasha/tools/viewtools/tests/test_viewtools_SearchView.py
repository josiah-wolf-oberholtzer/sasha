from pyramid import testing
from sasha.tools import viewtools
import sasha
import unittest


class SearchViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_SearchView_01(self):
        request = testing.DummyRequest()
        view = viewtools.SearchView(request)
        info = view()
        self.assertEqual(info['body_class'], 'search')
        self.assertEqual(info['title'], 'SASHA | Search')

    def test_SearchView_02(self):
        request = testing.DummyRequest(params={'order_by': 'md5'})
        view = viewtools.SearchView(request)
        info = view()
        event_names = list((_.name, _.md5) for _ in info['paginator'])
        self.assertEqual(event_names, [
            (u'event__alto_saxophone__kientzy_26__w_8va__t1.aif', u'0aa871cc374134068f406ede8cdc1354'),
            (u'event__alto_saxophone__kientzy_19__t2.aif', u'2be8a97d2e6ff00ccf543f1dede84f25'),
            (u'event__alto_saxophone__kientzy_26__w_8va__t2.aif', u'5adacef1895593f34ad6f29cd2b2f4e0'),
            (u'event__soprano_saxophone__br_073.aif', u'5b3d4c48fd38c64d91a1a725a67309e2'),
            (u'event__alto_saxophone__kientzy_47__t3.aif', u'65da0b6f1a19e9127cda338791dc3762'),
            (u'event__alto_saxophone__kientzy_47__t2.aif', u'759dd00332d47f8ebf91e13be032761d'),
            (u'event__soprano_saxophone__chromatic_scale_a4.aif', u'76c561c3f468ecc19f109ef98ef625a3'),
            (u'event__alto_saxophone__kientzy_19__t1.aif', u'8392c0fe1757176599241a80ee9fba13'),
            (u'event__alto_saxophone__br_123.aif', u'8709ef97e0e161e832d1628bc35f3089'),
            (u'event__alto_saxophone__kientzy_47__t1.aif', u'8a1dfa743464dc2ce55e0d212c4c324d'),
            (u'event__alto_saxophone__br_042.aif', u'bae113a08990072eb1bfd9c85b8cce34'),
            (u'event__alto_saxophone__kientzy_19__t3.aif', u'f316c1fb80ca7c550fbf57dd6b1bf4ca'),
            ])

    def test_SearchView_03(self):
        request = testing.DummyRequest(params={'order_by': 'spectral_centroid'})
        view = viewtools.SearchView(request)
        info = view()
        events = list(info['paginator'])
        event_names = [_.name for _ in events]
        descriptors = [_.descriptors.spectral_centroid for _ in events]
        self.assertEqual(event_names, [
            u'event__alto_saxophone__kientzy_19__t1.aif',
            u'event__alto_saxophone__kientzy_47__t1.aif',
            u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
            u'event__alto_saxophone__kientzy_47__t2.aif',
            u'event__alto_saxophone__kientzy_19__t2.aif',
            u'event__soprano_saxophone__br_073.aif',
            u'event__alto_saxophone__kientzy_47__t3.aif',
            u'event__alto_saxophone__br_042.aif',
            u'event__alto_saxophone__kientzy_19__t3.aif',
            u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
            u'event__soprano_saxophone__chromatic_scale_a4.aif',
            u'event__alto_saxophone__br_123.aif',
            ])
        self.assertAlmostEqual(descriptors[0], 427.48599731362873)
        self.assertAlmostEqual(descriptors[1], 428.5720050601167)
        self.assertAlmostEqual(descriptors[2], 535.4457268047546)
        self.assertAlmostEqual(descriptors[3], 621.4469657297443)
        self.assertAlmostEqual(descriptors[4], 651.9741133257897)
        self.assertAlmostEqual(descriptors[5], 740.5378291954424)
        self.assertAlmostEqual(descriptors[6], 762.2123493774226)
        self.assertAlmostEqual(descriptors[7], 783.7433598705129)
        self.assertAlmostEqual(descriptors[8], 834.7059641208233)
        self.assertAlmostEqual(descriptors[9], 841.0573636793752)
        self.assertAlmostEqual(descriptors[10], 892.1187465661267)
        self.assertAlmostEqual(descriptors[11], 1434.896511826344)

    def test_SearchView_04(self):
        request = testing.DummyRequest(params={'order_by': 'spectral_flatness'})
        view = viewtools.SearchView(request)
        info = view()
        events = list(info['paginator'])
        event_names = [_.name for _ in events]
        descriptors = [_.descriptors.spectral_flatness for _ in events]
        self.assertEqual(event_names, [
            u'event__soprano_saxophone__chromatic_scale_a4.aif',
            u'event__alto_saxophone__kientzy_19__t2.aif',
            u'event__alto_saxophone__kientzy_47__t2.aif',
            u'event__alto_saxophone__kientzy_47__t1.aif',
            u'event__alto_saxophone__kientzy_26__w_8va__t2.aif',
            u'event__alto_saxophone__kientzy_26__w_8va__t1.aif',
            u'event__soprano_saxophone__br_073.aif',
            u'event__alto_saxophone__kientzy_19__t1.aif',
            u'event__alto_saxophone__br_042.aif',
            u'event__alto_saxophone__kientzy_19__t3.aif',
            u'event__alto_saxophone__kientzy_47__t3.aif',
            u'event__alto_saxophone__br_123.aif',
            ])
        self.assertAlmostEqual(descriptors[0], 6.133884443473832e-06)
        self.assertAlmostEqual(descriptors[1], 6.514721098324684e-06)
        self.assertAlmostEqual(descriptors[2], 6.684449488983703e-06)
        self.assertAlmostEqual(descriptors[3], 1.484247381410036e-05)
        self.assertAlmostEqual(descriptors[4], 2.172923157666239e-05)
        self.assertAlmostEqual(descriptors[5], 2.2554557049246036e-05)
        self.assertAlmostEqual(descriptors[6], 2.4911581005520397e-05)
        self.assertAlmostEqual(descriptors[7], 2.6801641813076304e-05)
        self.assertAlmostEqual(descriptors[8], 4.2476256099637914e-05)
        self.assertAlmostEqual(descriptors[9], 4.629470463010788e-05)
        self.assertAlmostEqual(descriptors[10], 6.498449590485768e-05)
        self.assertAlmostEqual(descriptors[11], 7.134360563288096e-05)

    def test_SearchView_05(self):
        request = testing.DummyRequest(params={
            'with_pitches': 'd4',
            'without_pitches': 'd4',
            })
        view = viewtools.SearchView(request)
        info = view()

    def test_SearchView_06(self):
        request = testing.DummyRequest(params={
            'with_pitch_classes': 'd',
            'without_pitch_classes': 'd',
            })
        view = viewtools.SearchView(request)
        info = view()