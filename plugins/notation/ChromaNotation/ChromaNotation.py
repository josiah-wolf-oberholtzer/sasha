from sasha.plugins.notation.Notation import Notation
from sasha.plugins.analysis import ChromaAnalysis


class ChromaNotation(Notation):

    __requires__ = ChromaAnalysis

    plugin_label = 'chroma'

    ### PRIVATE METHODS ###

    def _build_lily(self, sublabel = None):
        from abjad.tools import scoretools
        from abjad.tools import stafftools
        from abjad.tools import voicetools
        from abjad.tools import contexttools
        from abjad.tools import markuptools
        from abjad.tools import notetools
        from abjad.tools import schemetools
        from abjad.tools import skiptools

        analysis = ChromaAnalysis(self)
        analysis.read()
        chroma_mean = self._normalize(analysis.mean)
        chroma_std = self._normalize(analysis.std)

        v_mean = voicetools.Voice([ ])
        v_std = voicetools.Voice([ ])
        staff = stafftools.Staff([v_mean, v_std])
        staff.is_parallel = True

        pitches = [x / 2. for x in range(0, 24)]

        v_mean.extend(notetools.make_notes(pitches, (1, 4)))
        v_std.extend(skiptools.Skip((1, 4)) * len(v_mean))

        for i, val in enumerate(chroma_mean):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            markuptools.Markup(markup, 'up')(v_mean[i])
            color = schemetools.SchemeColor('grey%d' % (90 - int(val * 90)))
            v_mean[i].override.text_script.color = color

        for i, val in enumerate(chroma_std):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            markuptools.Markup(markup, 'down')(v_std[i])
            color = schemetools.SchemeColor('grey%d' % (90 - int(val * 90)))
            v_std[i].override.text_script.color = color

        v_mean.override.text_script.staff_padding = 1.5
        v_std.override.text_script.staff_padding = 3.0

        staff.override.stem.transparent = True
        staff.engraver_removals.append('Time_signature_engraver')
        staff.engraver_removals.append('Bar_engraver')
        score = scoretools.Score([staff])
        contexttools.set_accidental_style_on_sequential_contexts_in_expr( \
            score, 'dodecaphonic')

        return score

    def _normalize(self, ndarray):
        nda = ndarray - ndarray.min()
        nda = nda / nda.max()
        return nda
