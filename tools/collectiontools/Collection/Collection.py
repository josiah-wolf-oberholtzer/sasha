from abjad import *
from sasha import Instrument
from sasha.core.mixins import _Immutable
from sasha.tools.diagramtools import SaxophoneFingeringDiagram


class Collection(_Immutable):

    __slots__ = ('_instrument', '_pairs')

    def __init__(self, instrument, pairs):
        assert isinstance(instrument, Instrument)
        assert instrument.idiom_schema is not None
        assert len(pairs)
        
        for pair in pairs:
            if not pitchtools.is_chromatic_pitch_name(pair[0]):
                raise ValueError('Expected pitch name, got %s' % pair[0])
            if not all([x in instrument.idiom_schema for x in pair[1]]):
                raise ValueError('Unexpected key name in %s' % pair[1])

        object.__setattr__(self, '_instrument', instrument)
        object.__setattr__(self, '_pairs', pairs)

    ### OVERRIDES ###

    def __getitem__(self, item):
        return self._pairs[item]

    def __iter__(self):
        for x in self._pairs:
            yield x

    def __len__(self):
        return len(self._pairs)

    ### PUBLIC ATTRIBUTES ###

    @property
    def instrument(self):
        return self._instrument

    ### PUBLIC METHOD ###

    def as_score(self):
        staff = Staff([ ])
        for pair in self:
            pitch, fingering = pair
            diagram = SaxophoneFingeringDiagram( )(fingering)
            note = Note(pitch, 1)
            markuptools.Markup(diagram, 'up')(note)
            staff.append(note)
        score = Score([staff])
        score.override.bar_number.break_visibility = schemetools.SchemeFunction("'#(#f #t #t)")
        score.override.bar_number.stencil = schemetools.SchemeFunction('(make-stencil-boxer 0.1 0.25 ly:text-interface::print)')
        score.override.time_signature.stencil = False
        score.set.bar_number_visibility = schemetools.SchemeFunction("all-bar-numbers-visible")
        marktools.LilyPondCommandMark('bar " "', 'before')(staff[0])
        return score
