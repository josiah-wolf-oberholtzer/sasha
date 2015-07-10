from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha import newdomaintools
from sasha.views.SearchView import SearchView
from webhelpers import paginate


@view_config(
    route_name='instrument',
    renderer='sasha:templates/instrument.mako',
    )
class InstrumentView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request
        instrument_name = self.request.matchdict['instrument_name']
        instrument_name = instrument_name.replace('-', ' ').title()
        try:
            self._instrument = newdomaintools.Instrument.objects.get(
                name=instrument_name,
                )
        except:
            message = '''SASHA can't figure out what kind of instrument '''
            message += '''<em>{!r}</em> might be.'''
            message = message.format(instrument_name)
            raise HTTPNotFound(message)
        self._idiom_parameters = self.process_idiom_params(
            self.instrument,
            self.request.params,
            )
        self._layout_parameters = self.process_layout_params(
            self.request.params,
            )
        self._pitch_parameters = self.process_pitch_params(
            self.request.params,
            )

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha import views
        query = self.query()
        paginator = views.Page(
            query,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url,
            )
        search_action = self.instrument.get_url(self.request)
        with_keys = ' '.join(
            x for x in self.idiom_parameters['with_keys'])
        without_keys = ' '.join(
            x for x in self.idiom_parameters['without_keys'])
        with_pitches = ' '.join(
            '{}{}'.format(x.pitch_class_name, x.octave_number)
            for x in self.pitch_parameters['with_pitches']
            )
        without_pitches = ' '.join(
            '{}{}'.format(x.pitch_class_name, x.octave_number)
            for x in self.pitch_parameters['without_pitches']
            )
        with_pitch_classes = ' '.join(
            str(x)
            for x in self.pitch_parameters['with_pitch_classes'],
            )
        without_pitch_classes = ' '.join(
            str(x)
            for x in self.pitch_parameters['without_pitch_classes'],
            )
        return {
            'body_class': 'search',
            'instrument': self.instrument,
            'instrument_name': self.instrument.name,
            'title': self.title,
            'paginator': paginator,
            'search_action': search_action,
            'with_keys': with_keys,
            'without_keys': without_keys,
            'with_pitches': with_pitches,
            'without_pitches': without_pitches,
            'with_pitch_classes': with_pitch_classes,
            'without_pitch_classes': without_pitch_classes,
            }

    ### PUBLIC METHODS ###

    def query(self):
        with_pitches = self.pitch_parameters.get('with_pitches')
        without_pitches = self.pitch_parameters.get('without_pitches')
        with_pitch_classes = self.pitch_parameters.get('with_pitch_classes')
        without_pitch_classes = self.pitch_parameters.get('without_pitch_classes')
        with_keys = self.idiom_parameters.get('with_keys')
        without_keys = self.idiom_parameters.get('without_keys')
        query = newdomaintools.Event.query_mongodb(
            instrument_name=self._instrument.name,
            with_keys=with_keys,
            with_pitch_classes=with_pitch_classes,
            with_pitches=with_pitches,
            without_keys=without_keys,
            without_pitch_classes=without_pitch_classes,
            without_pitches=without_pitches,
            )
        return query

    ### PUBLIC ATTRIBUTES ###

    @property
    def events(self):
        return newdomaintools.Event.objects(fingering__instrument=self.instrument)

    @property
    def idiom_parameters(self):
        return self._idiom_parameters

    @property
    def instrument(self):
        return self._instrument

    @property
    def layout_parameters(self):
        return self._layout_parameters

    @property
    def page_number(self):
        return int(self.layout_parameters['page'])

    @property
    def page_size(self):
        return int(self.layout_parameters['n'])

    @property
    def title(self):
        return 'SASHA | Instrument: %s' % self.instrument.name

    @property
    def page_url(self):
        return paginate.PageURL_WebOb(self.request)

    @property
    def pitch_parameters(self):
        return self._pitch_parameters

    @property
    def request(self):
        return self._request