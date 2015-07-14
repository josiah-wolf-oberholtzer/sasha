from pyramid import testing
from sasha.tools import viewtools
import sasha
import unittest


class ClusterViewTests(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        sasha.sasha_configuration.environment = 'testing'
        self.config = testing.setUp()
        self.config.include('sasha')

    def tearDown(self):
        testing.tearDown()

    def test_ClusterView_01(self):
        cluster = sasha.Cluster.objects.first()
        request = testing.DummyRequest(
            matchdict={
                'feature': cluster.feature,
                'cluster_id': cluster.cluster_id,
                },
            )
        view = viewtools.ClusterView(request)
        info = view()
        self.assertEqual(info['body_class'], 'clusters')
        self.assertEqual(
            info['title'],
            'SASHA | {} Cluster No.{}'.format(
                cluster.title_case_feature,
                cluster.cluster_id,
                ),
            )