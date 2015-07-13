from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha.tools import modeltools
from sasha.tools.viewtools.SearchView import SearchView
from webhelpers import paginate


@view_config(
    route_name='instrument',
    renderer='sasha:templates/instrument.mako',
    )
class InstrumentView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        SearchView.__init__(self, request)
        instrument_name = self.request.matchdict['instrument_name']
        instrument_name = instrument_name.replace('-', ' ').title()
        try:
            self._instrument = modeltools.Instrument.objects.get(
                name=instrument_name,
                )
        except:
            message = '''SASHA can't figure out what kind of instrument '''
            message += '''<em>{!r}</em> might be.'''
            message = message.format(instrument_name)
            raise HTTPNotFound(message)
        (
            with_keys,
            without_keys,
            ) = self.process_idiom_parameters(
            self.instrument,
            self.request.params,
            )
        self.search_parameters['instrument_name'] = self.instrument.name
        self.search_parameters['with_keys'] = with_keys
        self.search_parameters['without_keys'] = without_keys

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha.tools import viewtools
        query = modeltools.Event.query_mongodb(**self.search_parameters)
        paginator = viewtools.Page(
            query,
            page=self.layout_parameters['page_number'],
            items_per_page=self.layout_parameters['page_size'],
            url=self.page_url,
            )
        search_action = self.instrument.get_url(self.request)
        return {
            'body_class': 'search',
            'instrument': self.instrument,
            'instrument_name': self.instrument.name,
            'title': self.title,
            'paginator': paginator,
            'search_action': search_action,
            'search_parameters': self.search_parameters,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def instrument(self):
        return self._instrument

    @property
    def title(self):
        return 'SASHA | Instrument: %s' % self.instrument.name