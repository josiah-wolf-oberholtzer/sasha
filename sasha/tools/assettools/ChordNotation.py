import abjad
from sasha.tools.assettools.ChordAnalysis import ChordAnalysis
from sasha.tools.assettools.Notation import Notation


class ChordNotation(Notation):

    ### CLASS VARIABLES ###

    __requires__ = ChordAnalysis
    __slots__ = ()
    asset_label = 'chord'

    ### PRIVATE METHODS ###

    def _make_illustration(self):
        pairs = self._get_pitches_and_colors()
        chord = abjad.Chord([pair[0] for pair in pairs], 1)
        for note_head in chord.note_heads:
            for pitch, color in pairs:
                if note_head.written_pitch == pitch:
                    color = abjad.schemetools.SchemeColor(
                        'grey{}'.format(color),
                        )
                    note_head.tweak.color = color
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