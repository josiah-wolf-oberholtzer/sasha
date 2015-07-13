from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha.tools import modeltools
from sasha.tools.viewtools.SearchView import SearchView


@view_config(
    route_name='cluster',
    renderer='sasha:templates/cluster.mako',
    )
class ClusterView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        SearchView.__init__(self, request)

        feature = self.request.matchdict['feature'].replace('-', '_')
        cluster_id = int(self.request.matchdict['cluster_id'])
        try:
            self._current_cluster = modeltools.Cluster.objects.get(
                feature=feature,
                cluster_id=cluster_id,
                )
        except:
            message = 'No such cluster <em>{} {}</em>'
            message = message.format(
                self.request.matchdict['feature'],
                int(self.request.matchdict['cluster_id']),
                )
            raise HTTPNotFound(message)
        self._events = tuple(sorted(self.current_cluster.events, key=lambda x: x.id))
        instrument_name = self.request.params.get('instrument')
        if instrument_name:
            instrument_name = instrument_name.replace('_', ' ').title()
            try:
                self._instrument = modeltools.Instrument.objects.get(
                    name=instrument_name,
                    )
            except:
                message = "SASHA can't figure out what kind of instrument "
                message += '<em>{!r}</em> might be.'.format(instrument_name)
                raise HTTPNotFound(message)
        else:
            self._instrument = None

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha.tools import viewtools
        query = modeltools.Event.objects(
            clusters=self.current_cluster,
            fingering__instrument=self.instrument,
            )
        paginator = viewtools.Page(
            query,
            page=self.layout_parameters['page_number'],
            items_per_page=self.layout_parameters['page_size'],
            url=self.page_url,
            )
        return {
            'all_clusters': self.all_clusters,
            'body_class': 'clusters',
            'current_cluster': self.current_cluster,
            'instrument': self.instrument,
            'paginator': paginator,
            'title': self.title,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def current_cluster(self):
        return self._current_cluster

    @property
    def all_clusters(self):
        clusters = {}
        for cluster in modeltools.Cluster.objects:
            if cluster.feature not in clusters:
                clusters[cluster.feature] = []
            clusters[cluster.feature].append(cluster)
        for v in clusters.values():
            v.sort(key=lambda x: x.cluster_id)
        return clusters

    @property
    def instrument(self):
        return self._instrument

    @property
    def title(self):
        return 'SASHA | {} Cluster No.{}'.format(
            self.current_cluster.title_case_feature,
            self.current_cluster.cluster_id,
            )