from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha import domaintools
from sashaweb import helpers
from sashaweb.views.SearchView import SearchView


@view_config(
    route_name='cluster',
    renderer='sashaweb:templates/cluster.mako',
    )
class ClusterView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request
        feature = self.request.matchdict['feature'].replace('-', '_')
        cluster_id = int(self.request.matchdict['cluster_id'])
        try:
            self._current_cluster = domaintools.Cluster.get_one(
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
                self._instrument = domaintools.Instrument.get_one(
                    name=instrument_name,
                    )
            except:
                message = "SASHA can't figure out what kind of instrument "
                message += '<em>{!r}</em> might be.'.format(instrument_name)
                raise HTTPNotFound(message)
        else:
            self._instrument = None
        self._layout_parameters = self.process_layout_params(
            self.request.params)

    ### SPECIAL METHODS ###

    def __call__(self):
        paginator = helpers.Page(self.events,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url)
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
        for cluster in domaintools.Cluster.get():
            if cluster.feature not in clusters:
                clusters[cluster.feature] = []
            clusters[cluster.feature].append(cluster)
        for v in clusters.values():
            v.sort(key=lambda x: x.cluster_id)
        return clusters

    @property
    def events(self):
        if self.instrument is None:
            return self._events
        return [
            event for event in self._events
            if event.instrument_id == self.instrument.id
            ]

    @property
    def instrument(self):
        return self._instrument

    @property
    def title(self):
        return 'SASHA | {} Cluster No.{}'.format(
            self.current_cluster.title_case_feature,
            self.current_cluster.cluster_id,
            )