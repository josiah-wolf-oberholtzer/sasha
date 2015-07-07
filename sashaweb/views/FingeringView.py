from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha import domaintools
from sasha import sasha_configuration
from sashaweb import helpers
from sashaweb.views.SearchView import SearchView


@view_config(
    route_name='fingering',
    renderer='sashaweb:templates/fingering.mako',
    )
class FingeringView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request
        instrument_name = self.request.matchdict['instrument_name']
        instrument_name = instrument_name.replace('-', ' ').title()
        try:
            self._instrument = domaintools.Instrument.get_one(
                name=instrument_name,
                )
        except:
            message = "SASHA couldn't figure out what kind of instrument "
            message += "<em>{}</em> might be."
            message = message.format(self.request.matchdict['instrument_name'])
            raise HTTPNotFound(message)
        compact_representation = self.request.matchdict['compact_representation']
        try:
            self._fingering = domaintools.Fingering.get_one(
                instrument=self.instrument,
                compact_representation=compact_representation,
                )
        except:
            message = "SASHA couldn't find any {} fingering whose compact "
            message += "representation is <em>{}</em>"
            message = message.format(
                instrument_name.lower(),
                compact_representation,
                )
            raise HTTPNotFound(message)
        self._instrument_keys = tuple(self.fingering.instrument_keys)
        self._layout_parameters = self.process_layout_params(self.request.params)
        self._pitch_parameters = self.process_pitch_params(self.request.params)

    ### SPECIAL METHODS ###

    def __call__(self):
        query = self.query()
        paginator = helpers.Page(
            query,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url,
            )
        instrument_keys = ' '.join([key.name for key in self.instrument_keys])
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
            'fingering': self.fingering,
            'fingerings': self.fingering.find_similar_fingerings(n=12),
            'instrument': self.instrument,
            'instrument_keys': instrument_keys,
            'instrument_name': self.instrument.name,
            'title': self.title,
            'paginator': paginator,
            'search_action': self.fingering.get_url(self.request),
            'with_pitches': with_pitches,
            'without_pitches': without_pitches,
            'with_pitch_classes': with_pitch_classes,
            'without_pitch_classes': without_pitch_classes,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def events(self):
        return domaintools.Event.get(fingering_id=self.fingering.id)

    @property
    def fingering(self):
        return self._fingering

    @property
    def instrument(self):
        return self._instrument

    @property
    def instrument_keys(self):
        return self._instrument_keys

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
        return 'SASHA | %s Fingering: %s' % (self.instrument.name,
            ' '.join([key.name for key in self.instrument_keys]))

    @property
    def request(self):
        return self._request

    ### PUBLIC METHODS ###

    def query(self):
        query = sasha_configuration.get_session().query(domaintools.Event)
        query = query.join(domaintools.Fingering)
        query = query.filter(domaintools.Fingering.id == self.fingering.id)
        with_pitches = self.pitch_parameters.get('with_pitches')
        without_pitches = self.pitch_parameters.get('without_pitches')
        if with_pitches or without_pitches:
            #print 'WITH_PITCHES: %r' % with_pitches
            #print 'WITHOUT_PITCHES: %r' % without_pitches
            query = query.intersect(
                domaintools.Event.query_pitches(
                    with_pitches,
                    without_pitches,
                    ),
                )
        with_pitch_classes = self.pitch_parameters.get('with_pitch_classes')
        without_pitch_classes = self.pitch_parameters.get('without_pitch_classes')
        if with_pitch_classes or without_pitch_classes:
            #print 'WITH_PITCH_CLASSES: %r' % with_pitch_classes
            #print 'WITHOUT_PITCH_CLASSES: %r' % without_pitch_classes
            query = query.intersect(
                domaintools.Event.query_pitch_classes(
                    with_pitch_classes,
                    without_pitch_classes,
                    ),
                )
        return query