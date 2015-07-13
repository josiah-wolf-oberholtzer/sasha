from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha.tools import modeltools
from sasha.tools.viewtools.SearchView import SearchView


@view_config(
    route_name='fingering',
    renderer='sasha:templates/fingering.mako',
    )
class FingeringView(SearchView):

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
            message = "SASHA couldn't figure out what kind of instrument "
            message += "<em>{}</em> might be."
            message = message.format(self.request.matchdict['instrument_name'])
            raise HTTPNotFound(message)
        compact_representation = self.request.matchdict['compact_representation']
        try:
            self._event = modeltools.Event.objects(
                fingering__compact_representation=compact_representation,
                ).first()
        except:
            message = "SASHA couldn't find any {} fingering whose compact "
            message += "representation is <em>{}</em>"
            message = message.format(
                instrument_name.lower(),
                compact_representation,
                )
            raise HTTPNotFound(message)

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha.tools import viewtools
        query = modeltools.Event.query_mongodb(**self.search_parameters)
        compact_representation = self.event.fingering.compact_representation
        query = query(fingering__compact_representation=compact_representation)
        query = query.order_by(self.layout_parameters['order_by'])
        paginator = viewtools.Page(
            query,
            page=self.layout_parameters['page_number'],
            items_per_page=self.layout_parameters['page_size'],
            url=self.page_url,
            )
        return {
            'body_class': 'search',
            'fingering': self.event.fingering,
            'fingerings': self.event.fingering.find_similar_fingerings(n=12),
            'instrument': self.instrument,
            'instrument_keys': ' '.join(self.event.fingering.key_names),
            'instrument_name': self.instrument.name,
            'title': self.title,
            'paginator': paginator,
            'search_action': self.event.fingering.get_url(self.request),
            'search_parameters': self.search_parameters,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def event(self):
        return self._event

    @property
    def fingering(self):
        return self._fingering

    @property
    def instrument(self):
        return self._instrument

    @property
    def title(self):
        return 'SASHA | {} Fingering: {}'.format(
            self.event.fingering.instrument.name,
            ' '.join(self.event.fingering.key_names),
            )