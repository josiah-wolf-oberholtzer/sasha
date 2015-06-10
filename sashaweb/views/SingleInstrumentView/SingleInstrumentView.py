from pyramid.view import view_config
from sasha import *
from sashaweb.helpers import InstrumentHelper
from sashaweb.views.SearchView import SearchView
from webhelpers import paginate


@view_config(route_name='single_instrument', renderer='sashaweb:views/SingleInstrumentView/single_instrument.mako')
class SingleInstrumentView(SearchView):

    def __init__(self, request):
        self._request = request

        instrument_name = self.request.matchdict['instrument_name'].replace('-', ' ').title( )
        try:
            self._instrument = Instrument.get_one(name=instrument_name)
        except:
            raise HTTPNotFound('''SASHA can't figure out what kind of instrument <em>"%s"</em> might be.''' %
                instrument_name)

        self._idiom_parameters = self.process_idiom_params(self.instrument, self.request.params)
        self._layout_parameters = self.process_layout_params(self.request.params)
        self._pitch_parameters = self.process_pitch_params(self.request.params)

    ### SPECIAL METHODS ###

    def __call__(self):

        query = self.query()

        paginator = paginate.Page(query,
            page=self.page_number,
            items_per_page=self.page_size,
            url=self.page_url)

        return {
            'body_class': 'search',
            'instrument': self.instrument,
            'instrument_name': self.instrument.name,
            'page_title': self.page_title,
            'paginator': paginator,
            'search_action': InstrumentHelper(self.instrument, self.request).url,
            'with_keys': ' '.join([x for x in self.idiom_parameters['with_keys']]),
            'without_keys': ' '.join([x for x in self.idiom_parameters['without_keys']]),
            'with_pitches': ' '.join(['%s%d' % (x.chromatic_pitch_class_name, x.octave_number)
                for x in self.pitch_parameters['with_pitches']]),
            'without_pitches': ' '.join(['%s%d' % (x.chromatic_pitch_class_name, x.octave_number)
                for x in self.pitch_parameters['without_pitches']]),
            'with_pitch_classes': ' '.join([str(x) for x in self.pitch_parameters['with_pitch_classes']]),
            'without_pitch_classes': ' '.join([str(x) for x in self.pitch_parameters['without_pitch_classes']]),
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def events(self):
        return Event.get(instrument=self.instrument)

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
    def page_title(self):
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

    ### PUBLIC METHODS ###
    
    def query(self):
        
        query = sasha_configuration.get_session().query(Event).join(Instrument).filter(Instrument.id==self.instrument.id)

        with_pitches = self.pitch_parameters.get('with_pitches')
        without_pitches = self.pitch_parameters.get('without_pitches')
        if with_pitches or without_pitches:

            #print 'WITH_PITCHES: %r' % with_pitches
            #print 'WITHOUT_PITCHES: %r' % without_pitches

            query = query.intersect(Event.query_pitches(with_pitches, without_pitches))
                        
        with_pitch_classes = self.pitch_parameters.get('with_pitch_classes')
        without_pitch_classes = self.pitch_parameters.get('without_pitch_classes')
        if with_pitch_classes or without_pitch_classes:

            #print 'WITH_PITCH_CLASSES: %r' % with_pitch_classes
            #print 'WITHOUT_PITCH_CLASSES: %r' % without_pitch_classes

            query = query.intersect(Event.query_pitch_classes(with_pitch_classes, without_pitch_classes))

        with_keys = self.idiom_parameters.get('with_keys')
        without_keys = self.idiom_parameters.get('without_keys')
        if with_keys or without_keys:

            #print 'WITH_KEYS: %r' % with_keys
            #print 'WITHOUT_KEYS: %r' % without_keys

            query = query.intersect(Event.query_keys(self.instrument.name, with_keys, without_keys))
            
        return query
