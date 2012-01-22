from sasha.plugins.notation._Notation import _Notation
from sasha.plugins.analysis import ChromaAnalysis


class ChromaNotation(_Notation):

    __requires__ = ChromaAnalysis

    plugin_label = 'chroma'

    ### PRIVATE METHODS ###

    def _build_lily(self, sublabel = None):
        from abjad import Score
        from abjad import Staff
        from abjad import Voice
        from abjad.tools.contexttools import set_accidental_style_on_sequential_contexts_in_expr
        from abjad.tools.markuptools import Markup
        from abjad.tools.notetools import make_notes
        from abjad.tools.schemetools import SchemeColor
        from abjad.tools.skiptools import Skip

        analysis = ChromaAnalysis(self)
        analysis.read( )
        chroma_mean = self._normalize(analysis.mean)
        chroma_std = self._normalize(analysis.std)

        v_mean = Voice([ ])
        v_std = Voice([ ])
        staff = Staff([v_mean, v_std])
        staff.is_parallel = True

        pitches = [x / 2. for x in range(0, 24)]

        v_mean.extend(make_notes(pitches, (1, 4)))
        v_std.extend(Skip((1, 4)) * len(v_mean))

        for i, val in enumerate(chroma_mean):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            Markup(markup, 'up')(v_mean[i])
            color = SchemeColor('grey%d' % (90 - int(val * 90)))
            v_mean[i].override.text_script.color = color

        for i, val in enumerate(chroma_std):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            Markup(markup, 'down')(v_std[i])
            color = SchemeColor('grey%d' % (90 - int(val * 90)))
            v_std[i].override.text_script.color = color

        v_mean.override.text_script.staff_padding = 1.5
        v_std.override.text_script.staff_padding = 3.0

        staff.override.stem.transparent = True
        staff.engraver_removals.add('Time_signature_engraver')
        staff.engraver_removals.add('Bar_engraver')
        score = Score([staff])
        set_accidental_style_on_sequential_contexts_in_expr( \
            score, 'dodecaphonic')

        return score

    def _normalize(self, ndarray):
        nda = ndarray - ndarray.min( )
        nda = nda / nda.max( )
        return nda
