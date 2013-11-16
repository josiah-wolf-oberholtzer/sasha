import abjad
import copy
from itertools import groupby

from sasha import Instrument
from sasha.plugins.notation.Notation import Notation
from sasha.plugins.analysis import ChordAnalysis


class ChordNotation(Notation):

    __requires__ = ChordAnalysis

    plugin_label = 'chord'
    plugin_sublabels = ('concert', 'transposed')

    ### PRIVATE METHODS ###

    def _build_lily(self):
        pairs = self._get_pitches_and_colors()
        chord = abjad.Chord([pair[0] for pair in pairs], 1)
        for note_head in chord.note_heads:
            for pitch, color in pairs:
                if note_head.written_pitch == pitch:
                    note_head.tweak.color = \
                        abjad.schemetools.SchemeColor('grey%d' % color)
        score, treble_staff, bass_staff = \
            abjad.scoretools.make_piano_sketch_score_from_leaves([chord])
        comment = abjad.indicatortools.LilyPondComment(
            str(self.client.name), 'before')
        abjad.attach(comment, score)
        return score

    def _get_pitches_and_colors(self):
        analysis = ChordAnalysis(self)
        assert analysis.exists
        analysis = analysis.read()

        color_scalar = 60
        pitches = [x[0] for x in analysis]
        abs_amplitudes = [abs(x[1]) for x in analysis]
        # there might only be one pitch returned, so don't normalize
        if 1 < len(analysis):
            norm_amplitudes = [(x - min(abs_amplitudes)) /
                (max(abs_amplitudes) - min(abs_amplitudes))
                for x in abs_amplitudes]
            colors = [color_scalar * x for x in norm_amplitudes]
        else:
            colors = [0]
        return zip(pitches, colors)

    ### PUBLIC METHODS ###

    def write(self, sublabel = None, **kwargs):
        lily = self._build_lily()
        object.__setattr__(self, '_asset', lily)
        transposed = self._build_lily()
        instrument = Instrument.get_one(id=self.client.instrument_id)
        transposition = abjad.pitchtools.NamedInterval(
            instrument.transposition)
        for leaf in abjad.iterate(transpose).by_leaf():
            pitchtools.transpose_pitch_carrier_by_melodic_interval(
                leaf, transposition)
        if sublabel is None:
            self._save_lily_to_png(lily, 'concert')
            self._save_lily_to_png(transposed, 'transposed')
        elif sublabel == 'concert':
            self._save_lily_to_png(lily, 'concert')
        elif sublabel == 'transposed':
            self._save_lily_to_png(transposed, 'transposed')
