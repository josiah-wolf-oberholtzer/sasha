from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from webhelpers.html import HTML


class ClusterHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Cluster):
            self._cluster = arg
        else:
            raise ValueError('Expected Cluster instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def cluster(self):
        return self._cluster

    @property
    def feature(self):
        feature = self.cluster.feature
        if '_' in feature:
            return '-'.join([x.capitalize() for x in feature.split('_')])
        return feature.upper()

    @property
    def link(self):
        return HTML.tag('a', href=self.url, c=str(self.cluster.cluster_id))

    @property
    def url(self):
        feature = self.cluster.feature.replace('_', '-')
        return self.request.route_url('single_cluster',
            feature=feature,
            cluster_id=self.cluster.cluster_id)

    @property
    def verbose_link(self):
        return HTML.tag('a', href=self.url, c='%s No.%d' %
            (self.feature, self.cluster.cluster_id))