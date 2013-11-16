import collections
import abjad
from sasha import Instrument
from sasha.core.mixins import _ImmutableDictionary
from sasha.tools.diagramtools import LilyPondSaxDiagram


class Collection(object):

    __slots__ = ('_instrument', '_pairs')

    def __init__(self, instrument_name, pairs):
        instrument = Instrument.get_one(name=instrument_name)

        pairs = list(pairs)
        for i, pair in enumerate(pairs):
            pitch = float(abjad.NamedPitch(pair[0]))
            fingering = tuple(pair[1])
            pairs[i] = (pitch, fingering)
        
        object.__setattr__(self, '_pairs', pairs)
        object.__setattr__(self, '_instrument', instrument)

    ### OVERRIDES ###

    def __iter__(self):
        for k, v in self._pairs:
            yield k, v

    def __len__(self):
        return len(self._pairs)

    ### PUBLIC ATTRIBUTES ###

    @property
    def instrument(self):
        return self._instrument

    ### PUBLIC METHOD ###

    def as_dict(self):
        return collections.OrderedDict(self._pairs)

    def as_score(self):
        staff = abjad.Staff([])
        for pitch, fingering in self._pairs:
            diagram = LilyPondSaxDiagram()(fingering)
            note = abjad.Note(pitch, 1)
            markup abjad.Markup(diagram, 'up')
            abjad.attach(markup, note)
            staff.append(note)
        override(staff).text_script.staff_padding = 2
        score = abjad.Score([staff])
        abjad.override(score).time_signature.stencil = False
#        score.set.bar_number_visibility = schemetools.SchemeFunction("all-bar-numbers-visible")
        bar_line = abjad.indicatortools.BarLine('|.')
        abjad.attach(bar_line, staff[-1])
        return score
