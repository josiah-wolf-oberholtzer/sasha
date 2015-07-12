from abjad.tools import pitchtools
from pyramid.view import view_config
from sasha.tools import models
from sasha.views.View import View
from webhelpers import paginate
from webhelpers.html import literal


@view_config(
    route_name='search',
    renderer='sasha:templates/search.mako',
    )
class SearchView(View):

    ### CLASS VARIABLES ###

    _order_options = ('asc', 'desc')

    _sortby_options = ('event', 'fingering', 'instrument')

    _view_options = ('grid', 'row')

    ### INITIALIZER ###

    def __init__(self, request):
        View.__init__(self, request)
        self._layout_parameters = self.process_layout_params(self.request.params)
        self._pitch_parameters = self.process_pitch_params(self.request.params)

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
        search_action = self.request.route_url('search')
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
            'title': self.title,
            'paginator': paginator,
            'search_action': search_action,
            'with_pitches': with_pitches,
            'without_pitches': without_pitches,
            'with_pitch_classes': with_pitch_classes,
            'without_pitch_classes': without_pitch_classes,
            }

    ### PUBLIC ATTRIBUTES ####

    @property
    def instrument_parameters(self):
        return self._layout_parameters

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
        return 'SASHA | Search'

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

    def process_idiom_params(self, instrument, params):
        '''Process idiom query parameters.

        Handles:

            * `with_keys`
            * `without_keys`

        `with_keys` and `without_keys` should be plus (+) delimited.

        Raises HTTPBadRequest on bogus instrument name.

        Warnings are added to the session flash queue.

        Returns dictionary of processed params.
        '''
        processed_params = {}
        if not isinstance(instrument, models.Instrument):
            if not isinstance(instrument, (str, unicode)):
                instrument = instrument.name
            instrument = models.Instrument.objects.get(name=instrument)
        with_keys = params.get('with_keys')
        if with_keys is not None:
            keys_to_process = str(with_keys).split()
            processed_keys = []
            bad_keys = []
            for key in keys_to_process:
                if key not in instrument.key_names:
                    processed_keys.append(key)
                else:
                    bad_keys.append(key)
            processed_params['with_keys'] = processed_keys
            if bad_keys:
                bad_keys = ('<em>{}</em>'.format(_) for _ in bad_keys)
                bad_keys = ', '.join(bad_keys)
                message = '{} has no key(s) named: {}'
                message = message.format(instrument.name, bad_keys)
                self.reqeust.session.flash(literal(message))
        else:
            processed_params['with_keys'] = []
        without_keys = params.get('without_keys')
        if without_keys is not None:
            keys_to_process = str(without_keys).split()
            processed_keys = []
            bad_keys = []
            for key in keys_to_process:
                if key not in instrument.key_names:
                    processed_keys.append(key)
                else:
                    bad_keys.append(key)
            processed_params['without_keys'] = processed_keys
            if bad_keys:
                bad_keys = ('<em>{}</em>'.format(_) for _ in bad_keys)
                bad_keys = ', '.join(bad_keys)
                message = '{} has no key(s) named: {}'
                message = message.format(instrument.name, bad_keys)
                self.reqeust.session.flash(literal(message))
        else:
            processed_params['without_keys'] = []
        key_intersection = set(processed_params['with_keys']).intersection(
            set(processed_params['without_keys']))
        if key_intersection:
            bad_keys = ('<em>{}</em>'.format(_) for _ in key_intersection)
            bad_keys = ', '.join(bad_keys)
            message = 'Included and dis-included keys overlap: {}'
            message = message.format(bad_keys)
            self.request.session.flash(literal(message))
        return processed_params

    def process_layout_params(self, params):
        '''Process page layout query parameters.

        Handles:

            * `n` (number of items)
            * `order` (`asc`, `desc`)
            * `page` (page number)
            * `sortby` (`event`, `fingering`, `instrument`)
            * `view` (`grid`, `row`)

        Warnings are added to the session flash queue.

        Returns dictionary of processed parameters.
        '''

        processed_params = {}

        # max number of items on page
        n = params.get('n')
        if n is not None:
            try:
                n = max(int(n), 1)
                processed_params['n'] = n
            except:
                processed_params['n'] = 20
        else:
            processed_params['n'] = 20

        # page order (ascending, descending)
        order = params.get('order')
        if order is not None and str(order) in self._order_options:
            processed_params['order'] = str(order)
        else:
            processed_params['order'] = 'asc'

        # page number
        page = params.get('page')
        if page is not None:
            try:
                page = max(int(page), 1)
                processed_params['page'] = page
            except:
                processed_params['page'] = 1
        else:
            processed_params['page'] = 1

        # column to sort by
        sortby = params.get('sortby')
        if sortby is not None and str(sortby) in self._sortby_options:
            processed_params['sortby'] = str(sortby)
        else:
            processed_params['sortby'] = 'event'

        # page view style
        view = params.get('view')
        if view is not None and str(view) in self._view_options:
            processed_params['view'] = str(view)
        else:
            processed_params['view'] = 'row'

        return processed_params

    def process_pitch_params(self, params):
        '''Process pitch and pitch class inclusion/exclusion query parameters.

        Handles:

            * `with_pitch_classes`
            * `with_pitches`
            * `without_pitch_classes`
            * `without_pitches`

        Pitch names should specify octave with an integer.
        All argument lists are plus-sign (+) delimited.

        Warnings are added to the session flash queue.

        Returns dictionary of processed parameters.
        '''

        processed_params = {}

        with_pitches = params.get('with_pitches')
        if with_pitches is not None:
            pitches_to_process = str(with_pitches).split()
            processed_pitches = []
            bad_pitches = []
            for pitch in pitches_to_process:
                pitch_class, octave = pitch[:-1], pitch[-1]
                if (
                    octave.isdigit() and
                    pitchtools.PitchClass.is_pitch_class_name(pitch_class)
                    ):
                    processed_pitches.append(pitchtools.NamedPitch(pitch_class, int(octave)))
                else:
                    bad_pitches.append(pitch)
            processed_params['with_pitches'] = sorted(processed_pitches)
            if bad_pitches:
                self.request.session.flash(literal(
                    'No such pitch name(s): %s' % ', '.join(['<em>%s</em>' % x for x in bad_pitches])))
        else:
            processed_params['with_pitches'] = []

        without_pitches = params.get('without_pitches')
        if without_pitches is not None:
            pitches_to_process = str(without_pitches).split()
            processed_pitches = []
            bad_pitches = []
            for pitch in pitches_to_process:
                pitch_class, octave = pitch[:-1], pitch[-1]
                if (
                    octave.isdigit() and
                    pitchtools.PitchClass.is_pitch_class_name(pitch_class)
                    ):
                    processed_pitches.append(pitchtools.NamedPitch(pitch_class, int(octave)))
                else:
                    bad_pitches.append(pitch)
            processed_params['without_pitches'] = sorted(processed_pitches)
            if bad_pitches:
                self.request.session.flash(literal(
                    'No such pitch name(s): %s' % ', '.join(['<em>%s</em>' % x for x in bad_pitches])))
        else:
            processed_params['without_pitches'] = []

        with_pitch_classes = params.get('with_pitch_classes')
        if with_pitch_classes is not None:
            pitch_classes_to_process = str(with_pitch_classes).split()
            processed_pitch_classes = []
            bad_pitch_classes = []
            for pitch_class in pitch_classes_to_process:
                if pitchtools.PitchClass.is_pitch_class_name(pitch_class):
                    processed_pitch_classes.append(pitchtools.NamedPitchClass(pitch_class))
                else:
                    bad_pitch_classes.append(pitch_class)
            processed_params['with_pitch_classes'] = sorted(processed_pitch_classes, key=lambda x: float(x))
            if bad_pitch_classes:
                self.request.session.flash(literal(
                    'No such pitch class name(s): %s' % ', '.join(['<em>%s</em>' % x for x in bad_pitch_classes])))
        else:
            processed_params['with_pitch_classes'] = []

        without_pitch_classes = params.get('without_pitch_classes')
        if without_pitch_classes is not None:
            pitch_classes_to_process = str(without_pitch_classes).split()
            processed_pitch_classes = []
            bad_pitch_classes = []
            for pitch_class in pitch_classes_to_process:
                if pitchtools.PitchClass.is_pitch_class_name(pitch_class):
                    processed_pitch_classes.append(pitchtools.NamedPitchClass(pitch_class))
                else:
                    bad_pitch_classes.append(pitch_class)
            processed_params['without_pitch_classes'] = sorted(processed_pitch_classes, key=lambda x: float(x))
            if bad_pitch_classes:
                self.request.session.flash(literal(
                    'No such pitch class name(s): %s' % ', '.join(['<em>%s</em>' % x for x in bad_pitch_classes])))
        else:
            processed_params['without_pitch_classes'] = []

        pitch_intersection = set(processed_params['with_pitches']).intersection(set(processed_params['without_pitches']))
        pitch_class_intersection = set(processed_params['with_pitch_classes']).intersection(set(processed_params['without_pitch_classes']))

        if pitch_intersection:
            self.request.session.flash(
                literal('Included and dis-included pitches overlap: %s' %
                    ' '.join(['<em>%s%d</em>' % (x.pitch_class_name, x.octave_number)
                    for x in pitch_intersection])))

        if pitch_class_intersection:
            self.request.session.flash(
                literal('Included and dis-included pitch classes overlap: %s' %
                    ' '.join(['<em>%s</em>' % x for x in pitch_class_intersection])))

        return processed_params

    def query(self):
        with_pitches = self.pitch_parameters.get('with_pitches')
        without_pitches = self.pitch_parameters.get('without_pitches')
        with_pitch_classes = self.pitch_parameters.get('with_pitch_classes')
        without_pitch_classes = self.pitch_parameters.get('without_pitch_classes')
        query = models.Event.query_mongodb(
            with_pitches=with_pitches,
            without_pitches=without_pitches,
            with_pitch_classes=with_pitch_classes,
            without_pitch_classes=without_pitch_classes,
            )
        return query