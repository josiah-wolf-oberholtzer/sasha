from pyramid.view import view_config
from sasha import *
from sashaweb.views.View import View


@view_config(
    route_name='all_clusters',
    renderer='sashaweb:templates/all_clusters.mako',
    )
class AllClustersView(View):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request

    ### SPECIAL METHODS ###

    def __call__(self):
        return {
            'clusters': self.clusters,
            'body_class': 'clusters',
            'title': self.title
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
    def title(self):
        return 'SASHA | All Clusters'