import abjad
from sasha.tools.assettools.Notation import Notation
from sasha.tools.assettools import ChromaAnalysis


class ChromaNotation(Notation):

    __requires__ = ChromaAnalysis

    plugin_label = 'chroma'

    ### PRIVATE METHODS ###

    def _make_illustration(self, sublabel = None):

        analysis = ChromaAnalysis(self)
        analysis.read()
        chroma_mean = self._normalize(analysis.mean)
        chroma_std = self._normalize(analysis.std)

        v_mean = abjad.Voice([ ])
        v_std = abjad.Voice([ ])
        staff = abjad.Staff([v_mean, v_std])
        staff.is_simultaneous = True

        pitches = [x / 2. for x in range(0, 24)]

        v_mean.extend(abjad.scoretools.make_notes(pitches, (1, 4)))
        v_std.extend(abjad.scoretools.Skip((1, 4)) * len(v_mean))

        for i, val in enumerate(chroma_mean):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            markup = abjad.Markup(markup, 'up')
            abjad.attach(markup, v_mean[i])
            color = abjad.schemetools.SchemeColor(
                'grey%d' % (90 - int(val * 90)))
            abjad.override(v_mean[i]).text_script.color = color
            #v_mean[i].override.text_script.color = color

        for i, val in enumerate(chroma_std):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val *  5.) + 0.75))
            markup = abjad.Markup(markup, 'down')
            abjad.attach(markup, v_std[i])
            color = abjad.schemetools.SchemeColor(
                'grey%d' % (90 - int(val * 90)))
            abjad.override(v_std[i]).text_script.color = color
            #v_std[i].override.text_script.color = color

        abjad.override(v_mean).text_script.staff_padding = 1.5
        #v_mean.override.text_script.staff_padding = 1.5
        abjad.override(v_std).text_script.staff_padding = 3.0
        #v_std.override.text_script.staff_padding = 3.0

        abjad.override(staff).stem.transparent = True
        #staff.override.stem.transparent = True
        staff.engraver_removals.append('Time_signature_engraver')
        staff.engraver_removals.append('Bar_engraver')
        score = abjad.Score([staff])
        #indicatortools.set_accidental_style_on_sequential_contexts_in_expr( \
        #    score, 'dodecaphonic')

        return score

    def _normalize(self, ndarray):
        nda = ndarray - ndarray.min()
        nda = nda / nda.max()
        return nda
