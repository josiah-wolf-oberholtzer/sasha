from abjad.tools import pitchtools
from pyramid.view import view_config
from sasha.tools import modeltools
from sasha.tools.viewtools.View import View
from webhelpers.html import literal


@view_config(
    route_name='search',
    renderer='sasha:templates/search.mako',
    )
class SearchView(View):

    ### INITIALIZER ###

    def __init__(self, request):
        View.__init__(self, request)
        (
            page_number,
            page_size,
            ) = self.process_layout_parameters(
            self.request.params)
        (
            with_pitches,
            without_pitches,
            ) = self.process_pitch_parameters(
            self.request.params)
        (
            with_pitch_classes,
            without_pitch_classes,
            ) = self.process_pitch_class_parameters(self.request.params)
        self._layout_parameters = {
            'page_number': page_number,
            'page_size': page_size,
            }
        self._search_parameters = {
            'with_pitches': with_pitches,
            'without_pitches': without_pitches,
            'with_pitch_classes': with_pitch_classes,
            'without_pitch_classes': without_pitch_classes,
            }

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
        search_action = self.request.route_url('search')
        with_pitches = ' '.join(
            '{}{}'.format(x.pitch_class_name, x.octave_number)
            for x in self.search_parameters['with_pitches']
            )
        without_pitches = ' '.join(
            '{}{}'.format(x.pitch_class_name, x.octave_number)
            for x in self.search_parameters['without_pitches']
            )
        with_pitch_classes = ' '.join(
            str(x)
            for x in self.search_parameters['with_pitch_classes'],
            )
        without_pitch_classes = ' '.join(
            str(x)
            for x in self.search_parameters['without_pitch_classes'],
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

    ### PUBLIC METHODS ###

    def process_idiom_parameters(self, instrument, params):
        if not isinstance(instrument, modeltools.Instrument):
            if not isinstance(instrument, (str, unicode)):
                instrument = instrument.name
            instrument = modeltools.Instrument.objects.get(name=instrument)
        bad_keys = set()
        with_keys = params.get('with_keys')
        processed_with_keys = set()
        if with_keys:
            keys_to_process = str(with_keys).split()
            for key in keys_to_process:
                if key not in instrument.key_names:
                    processed_with_keys.add(key)
                else:
                    bad_keys.add(key)
        without_keys = params.get('without_keys')
        processed_without_keys = set()
        if without_keys:
            keys_to_process = str(without_keys).split()
            for key in keys_to_process:
                if key not in instrument.key_names:
                    processed_without_keys.add(key)
                else:
                    bad_keys.add(key)
        if bad_keys:
            bad_keys = ('<em>{}</em>'.format(_) for _ in bad_keys)
            bad_keys = ', '.join(bad_keys)
            message = '{} has no key(s) named: {}'
            message = message.format(instrument.name, bad_keys)
            self.reqeust.session.flash(literal(message))
        key_intersection = processed_with_keys.union(processed_without_keys)
        if key_intersection:
            bad_keys = ('<em>{}</em>'.format(_) for _ in key_intersection)
            bad_keys = ', '.join(bad_keys)
            message = 'Included and dis-included keys overlap: {}'
            message = message.format(bad_keys)
            self.request.session.flash(literal(message))
        return processed_with_keys, processed_without_keys

    def process_pitches(self, pitches_to_process):
        processed_pitches = []
        bad_pitches = []
        if pitches_to_process:
            pitches_to_process = str(pitches_to_process).split()
            for pitch in pitches_to_process:
                pitch_class, octave = pitch[:-1], pitch[-1]
                if (
                    octave.isdigit() and
                    pitchtools.PitchClass.is_pitch_class_name(pitch_class)
                    ):
                    pitch = pitchtools.NamedPitch(pitch_class, int(octave))
                    processed_pitches.append(pitch)
                else:
                    bad_pitches.append(pitch)
        processed_pitches = set(processed_pitches)
        bad_pitches = set(bad_pitches)
        return processed_pitches, bad_pitches

    def process_pitch_classes(self, pitch_classes_to_process):
        processed_pitch_classes = []
        bad_pitch_classes = []
        if pitch_classes_to_process:
            pitch_classes_to_process = str(pitch_classes_to_process).split()
            for pitch_class in pitch_classes_to_process:
                if pitchtools.PitchClass.is_pitch_class_name(pitch_class):
                    pitch_class = pitchtools.NamedPitchClass(pitch_class)
                    processed_pitch_classes.append(pitch_class)
                else:
                    bad_pitch_classes.append(pitch_class)
        processed_pitch_classes = set(processed_pitch_classes)
        bad_pitch_classes = set(bad_pitch_classes)
        return processed_pitch_classes, bad_pitch_classes

    def process_layout_parameters(self, params):
        page_size = params.get('n', 20)
        if page_size:
            try:
                page_size = max(int(page_size), 1)
            except:
                page_size = 20
        else:
            page_size = 20
        page_number = params.get('page', 1)
        if page_number:
            try:
                page_number = max(int(page_number), 1)
            except:
                page_number = 1
        else:
            page_number = 1
        return int(page_number), int(page_size)

    def process_pitch_parameters(self, params):
        with_pitches, bad_with_pitches = self.process_pitches(
            params.get('with_pitches', []))
        without_pitches, bad_without_pitches = self.process_pitches(
            params.get('without_pitches', []))
        bad_pitches = bad_with_pitches.union(bad_without_pitches)
        if bad_pitches:
            bad_pitches = ('<em>{}</em>'.format(_) for _ in bad_pitches)
            bad_pitches = ', '.join(bad_pitches)
            message = 'No such pitch name(s): {}'.format(bad_pitches)
            self.request.session.flash(literal(message))
        pitch_intersection = with_pitches.intersection(without_pitches)
        if pitch_intersection:
            bad_pitches = ('<em>{}{}</em>'.format(
                _.pitch_class_name, _.octave_number)
                for _ in pitch_intersection
                )
            message = 'Included and dis-included pitches overlap: {}'
            message = message.format(bad_pitches)
            self.request.session.flash(literal(message))
        return with_pitches, without_pitches

    def process_pitch_class_parameters(self, params):
        with_pitch_classes, bad_with_pitch_classes = \
            self.process_pitch_classes(params.get('with_pitch_classes', []))
        without_pitch_classes, bad_without_pitch_classes = \
            self.process_pitch_classes(params.get('without_pitch_classes', []))
        bad_pitch_classes = bad_with_pitch_classes.union(
            bad_without_pitch_classes)
        if bad_pitch_classes:
            bad_pitch_classes = ('<em>{}</em>'.format(_) for _ in bad_pitch_classes)
            bad_pitch_classes = ', '.join(bad_pitch_classes)
            message = 'No such pitch-class name(s): {}'.format(bad_pitch_classes)
            self.request.session.flash(literal(message))
        pitch_class_intersection = with_pitch_classes.intersection(
            without_pitch_classes)
        if pitch_class_intersection:
            bad_pitch_classes = ('<em>{}{}</em>'.format(
                _.pitch_class_name, _.octave_number)
                for _ in pitch_class_intersection
                )
            message = 'Included and dis-included pitch-classes overlap: {}'
            message = message.format(bad_pitch_classes)
            self.request.session.flash(literal(message))
        return with_pitch_classes, without_pitch_classes

    ### PUBLIC ATTRIBUTES ####

    @property
    def layout_parameters(self):
        return self._layout_parameters

    @property
    def search_parameters(self):
        return self._search_parameters

    @property
    def title(self):
        return 'SASHA | Search'