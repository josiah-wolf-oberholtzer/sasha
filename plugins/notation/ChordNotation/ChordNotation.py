from itertools import groupby
from sasha.plugins.notation._Notation import _Notation
from sasha.plugins.analysis import ChordAnalysis


class ChordNotation(_Notation):

    _label = 'chord'
    _requires = (ChordAnalysis,)
    _sublabels = ('concert', 'transposed')

    ### PRIVATE METHODS ###

    def _build_lily(self):
        from abjad import Chord
        from abjad.tools.marktools import LilyPondComment
        from abjad.tools.schemetools import SchemeColor
        from abjad.tools.scoretools import make_piano_sketch_score_from_leaves

        pairs = self._get_pitches_and_colors( )
        chord = Chord([pair[0] for pair in pairs], 1)
        for note_head in chord.note_heads:
            for pitch, color in pairs:
                if note_head.written_pitch == pitch:
                    note_head.tweak.color = SchemeColor('grey%d' % color)
        score, treble_staff, bass_staff = make_piano_sketch_score_from_leaves([chord])
        LilyPondComment(self.event.name, 'before')(score)

        return score

    def _get_pitches_and_colors(self):
        analysis = ChordAnalysis(self).read( )
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
        try:
            lily = self._build_lily( )
            object.__setattr__(self, '_asset', lily)
            self._save_lily_to_png(lily, 'concert')
        except:
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info( )
            print '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
