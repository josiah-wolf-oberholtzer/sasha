import abjad
from sasha.tools.assettools.Notation import Notation
from sasha.tools.assettools.ChromaAnalysis import ChromaAnalysis


class ChromaNotation(Notation):

    ### CLASS VARIABLES ###

    __requires__ = ChromaAnalysis
    __slots__ = ()
    plugin_label = 'chroma'

    ### PRIVATE METHODS ###

    def _make_illustration(self, sublabel=None):
        analysis = ChromaAnalysis(self)
        analysis.read()
        chroma_mean = self._normalize(analysis.mean)
        chroma_std = self._normalize(analysis.std)
        v_mean = abjad.Voice([])
        v_std = abjad.Voice([])
        staff = abjad.Staff([v_mean, v_std])
        staff.is_simultaneous = True
        pitches = [x / 2. for x in range(0, 24)]
        v_mean.extend(abjad.scoretools.make_notes(pitches, (1, 4)))
        v_std.extend(abjad.scoretools.Skip((1, 4)) * len(v_mean))
        for i, val in enumerate(chroma_mean):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val * 5.) + 0.75))
            markup = abjad.Markup(markup, 'up')
            abjad.attach(markup, v_mean[i])
            color = abjad.schemetools.SchemeColor(
                'grey%d' % (90 - int(val * 90)))
            abjad.override(v_mean[i]).text_script.color = color
        for i, val in enumerate(chroma_std):
            markup = "\\filled-box #'(0 . 1.25) #'(%s . %s) #1" % \
                (str((val * -5.) - 0.75),
                 str((val * 5.) + 0.75))
            markup = abjad.Markup(markup, 'down')
            abjad.attach(markup, v_std[i])
            color = abjad.schemetools.SchemeColor(
                'grey%d' % (90 - int(val * 90)))
            abjad.override(v_std[i]).text_script.color = color
        abjad.override(v_mean).text_script.staff_padding = 1.5
        abjad.override(v_std).text_script.staff_padding = 3.0
        abjad.override(staff).stem.transparent = True
        staff.remove_commands.append('Time_signature_engraver')
        staff.remove_commands.append('Bar_engraver')
        score = abjad.Score([staff])
        illustration = score.__illustrate__()
        return illustration

    def _normalize(self, ndarray):
        nda = ndarray - ndarray.min()
        nda = nda / nda.max()
        return nda