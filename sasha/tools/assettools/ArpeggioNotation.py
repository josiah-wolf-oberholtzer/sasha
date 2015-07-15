import abjad
from sasha.tools.assettools.ChordAnalysis import ChordAnalysis
from sasha.tools.assettools.Notation import Notation


class ArpeggioNotation(Notation):

    ### CLASS VARIABLES ###

    __requires__ = ChordAnalysis
    __slots__ = ()
    asset_label = 'arpeggio'

    ### PRIVATE METHODS ###

    def _make_illustration(self):
        pitches, colors = self._get_pitches_and_colors()
        notes = abjad.scoretools.make_notes(pitches, [(1, 4)])
        for note, color in zip(notes, colors):
            color = abjad.schemetools.SchemeColor('grey{}'.format(color))
            abjad.override(note).note_head.color = color
        expr = abjad.scoretools.make_piano_sketch_score_from_leaves(notes)
        score = expr[0]
        abjad.override(score).stem.transparent = True
        abjad.override(score).rest.transparent = True
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
        colors = [int(_) for _ in colors]
        pairs = sorted(zip(colors, pitches))
        colors = [_[0] for _ in pairs]
        pitches = [_[1] for _ in pairs]
        return pitches, colors