from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha import sasha_configuration
from sasha.tools import modeltools
from sasha.tools.viewtools.SearchView import SearchView


@view_config(
    route_name='fingering',
    renderer='sasha:templates/fingering.mako',
    )
class FingeringView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request
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
        self._layout_parameters = self.process_layout_params(self.request.params)
        self._pitch_parameters = self.process_pitch_params(self.request.params)

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha.tools import viewtools
        query = self.query()
        paginator = viewtools.Page(
            query,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url,
            )
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
            'fingering': self.event.fingering,
            'fingerings': self.event.fingering.find_similar_fingerings(n=12),
            'instrument': self.instrument,
            'instrument_keys': ' '.join(self.event.fingering.key_names),
            'instrument_name': self.instrument.name,
            'title': self.title,
            'paginator': paginator,
            'search_action': self.event.fingering.get_url(self.request),
            'with_pitches': with_pitches,
            'without_pitches': without_pitches,
            'with_pitch_classes': with_pitch_classes,
            'without_pitch_classes': without_pitch_classes,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def event(self):
        return self._event

    @property
    def events(self):
        return modeltools.Event.objects(fingering=self.event.fingering)

    @property
    def fingering(self):
        return self._fingering

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
        return 'SASHA | {} Fingering: {}'.format(
            self.event.fingering.instrument.name,
            ' '.join(self.event.fingering.key_names),
            )

    @property
    def request(self):
        return self._request

    ### PUBLIC METHODS ###

    def query(self):
        with_pitches = self.pitch_parameters.get('with_pitches')
        without_pitches = self.pitch_parameters.get('without_pitches')
        with_pitch_classes = self.pitch_parameters.get('with_pitch_classes')
        without_pitch_classes = self.pitch_parameters.get('without_pitch_classes')
        query = modeltools.Event.query_mongodb(
            with_pitches=with_pitches,
            without_pitches=without_pitches,
            with_pitch_classes=with_pitch_classes,
            without_pitch_classes=without_pitch_classes,
            )
        compact_representation = self.event.fingering.compact_representation
        query = query(fingering__compact_representation=compact_representation)
        return query