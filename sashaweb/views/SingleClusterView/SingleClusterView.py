from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha import *
from sashaweb.views.SearchView import SearchView
from webhelpers import paginate


@view_config(route_name='single_cluster', renderer='sashaweb:views/SingleClusterView/single_cluster.mako')
class SingleClusterView(SearchView):

    def __init__(self, request):
        self._request = request
        self._layout_parameters = self.process_layout_params(self.request.params)

        feature = self.request.matchdict['feature'].replace('-', '_')
        cluster_id = int(self.request.matchdict['cluster_id'])

        try:
            self._cluster = Cluster.get_one(feature=feature, cluster_id=cluster_id)
        except:
            raise HTTPNotFound("No such cluster <em>%s %d</em>" %
                (self.request.matchdict['feature'],
                int(self.request.matchdict['cluster_id'])))

        self._events = tuple(sorted(self.cluster.events, key=lambda x: x.id))

        instrument_name = self.request.params.get('instrument')
        if instrument_name is not None:
            instrument_name = instrument_name.replace('_', ' ').title( )
            try:
                self._instrument = Instrument.get_one(name=instrument_name)
            except:
                raise HTTPNotFound('''SASHA can't figure out what kind of instrument <em>"%s"</em> might be.''' %
                    instrument_name)
        else:
            self._instrument = None

    ### SPECIAL METHODS ###

    def __call__(self):

        paginator = paginate.Page(self.events,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url)

        return {
            'body_class': 'clusters',
            'cluster': self.cluster,
            'clusters': self.clusters,
            'instrument': self.instrument,
            'page_title': self.page_title,
            'paginator': paginator,
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def cluster(self):
        return self._cluster

    @property
    def clusters(self):
        clusters = { }
        for cluster in Cluster.get():
            if cluster.feature not in clusters:
                clusters[cluster.feature] = [ ]
            clusters[cluster.feature].append(cluster)
        for v in clusters.values():
            v.sort(key=lambda x: x.cluster_id)
        return clusters

    @property
    def events(self):
        if self.instrument is None:
            return self._events
        else:
            return [event for event in self._events if event.instrument_id == self.instrument.id]

    @property
    def instrument(self):
        return self._instrument

    @property
    def page_title(self):
        return 'SASHA | %s Cluster No.%d' % (self.cluster.feature.upper(), self.cluster.cluster_id)
