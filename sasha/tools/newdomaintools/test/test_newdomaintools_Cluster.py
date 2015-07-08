# -*- encoding: utf-8 -*-
from pyramid import testing
import sasha
import unittest


class ClusterTests(unittest.TestCase):

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_Cluster_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        self.assertEqual(cluster.cluster_id, 1)
        self.assertEqual(cluster.feature, 'chroma')
        self.assertEqual(len(cluster.events), 1)

    def test_Cluster_dash_case_feature_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        self.assertEqual(cluster.dash_case_feature, 'chroma')

    def test_Cluster_get_long_link_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        long_link = cluster.get_long_link(request)
        self.assertEqual(
            long_link.encode('utf-8'),
            '<a href="http://example.com/clusters/chroma/1/">Chroma № 1</a>',
            )

    def test_Cluster_get_long_link_02(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=5,
            feature='constant_q',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        long_link = cluster.get_long_link(request)
        self.assertEqual(
            long_link.encode('utf-8'),
            '<a href="http://example.com/clusters/constant-q/5/">Constant-Q № 5</a>',
            )

    def test_Cluster_get_short_link_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        short_link = cluster.get_short_link(request)
        self.assertEqual(
            short_link.encode('utf-8'),
            '<a href="http://example.com/clusters/chroma/1/">№ 1</a>',
            )

    def test_Cluster_get_short_link_02(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=5,
            feature='constant_q',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        short_link = cluster.get_short_link(request)
        self.assertEqual(
            short_link.encode('utf-8'),
            '<a href="http://example.com/clusters/constant-q/5/">№ 5</a>',
            )

    def test_Cluster_get_url_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        url = cluster.get_url(request)
        self.assertEqual(url, 'http://example.com/clusters/chroma/1/')

    def test_Cluster_get_url_02(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=5,
            feature='constant_q',
            )
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        url = cluster.get_url(request)
        self.assertEqual(url, 'http://example.com/clusters/constant-q/5/')

    def test_Cluster_long_link_text_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        self.assertEqual(cluster.long_link_text, 'Chroma № 1')

    def test_Cluster_short_link_text_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        self.assertEqual(cluster.short_link_text, '№ 1')

    def test_Cluster_title_case_feature_01(self):
        cluster = sasha.newdomaintools.Cluster.objects.get(
            cluster_id=1,
            feature='chroma',
            )
        self.assertEqual(cluster.title_case_feature, 'Chroma')