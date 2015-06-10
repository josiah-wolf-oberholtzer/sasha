from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from sasha import *
from sashaweb.views._View import _View
from webhelpers import paginate
from webhelpers.html import literal


@view_config(route_name='all_clusters', renderer='sashaweb:views/AllClustersView/all_clusters.mako')
class AllClustersView(_View):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request

    ### SPECIAL METHODS ###

    def __call__(self):

        return {
            'clusters': self.clusters,
            'body_class': 'clusters',
            'page_title': self.page_title
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def clusters(self):
        clusters = {}
        for cluster in Cluster.get():
            if cluster.feature not in clusters:
                clusters[cluster.feature] = []
            clusters[cluster.feature].append(cluster)
        for v in clusters.values():
            v.sort(key=lambda x: x.cluster_id)
        return clusters

    @property
    def page_title(self):
        return 'SASHA | All Clusters'
