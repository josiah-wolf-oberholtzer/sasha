from abjad import *
from sasha import Instrument
from sasha.core.mixins import _Immutable
from sasha.tools.diagramtools import LilyPondSaxDiagram


class Collection(_Immutable):

    __slots__ = ('_instrument', '_pairs')

    def __init__(self, instrument_name, pairs):
        instrument = Instrument.get_one(name=instrument_name)

        pairs = list(pairs)
        for i, pair in enumerate(pairs):
            pitch = pitchtools.NamedChromaticPitch(pair[0])
            fingering = pair[1]
            pairs[i] = tuple([pitch, fingering])
        pairs = tuple(pairs)

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
            diagram = LilyPondSaxDiagram( )(fingering)
            note = Note(pitch, 1)
            markuptools.Markup(diagram, 'up')(note)
            staff.append(note)
        staff.override.text_script.staff_padding = 2
        score = Score([staff])
        score.override.time_signature.stencil = False
#        score.set.bar_number_visibility = schemetools.SchemeFunction("all-bar-numbers-visible")
        marktools.BarLine('|.')(staff[-1])
        return score
