from abjad import attach
from abjad import override
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools import scoretools
from sasha.tools.assettools.Notation import Notation
from sasha.tools.assettools.ChromaAnalysis import ChromaAnalysis


class ChromaNotation(Notation):

    ### CLASS VARIABLES ###

    __requires__ = ChromaAnalysis
    __slots__ = ()
    plugin_label = 'chroma'

    ### PRIVATE METHODS ###

    def _make_illustration(self):
        analysis = ChromaAnalysis(self)
        analysis.read()
        chroma_mean = self._normalize(analysis.mean)
        chroma_std = self._normalize(analysis.std)
        v_mean = scoretools.Voice([])
        v_std = scoretools.Voice([])
        staff = scoretools.Staff([v_mean, v_std])
        staff.is_simultaneous = True
        pitches = [x / 2. for x in range(0, 24)]
        v_mean.extend(scoretools.make_notes(pitches, (1, 4)))
        v_std.extend(scoretools.Skip((1, 4)) * len(v_mean))
        for i, val in enumerate(chroma_mean):
            x_extent = (0, 1.25)
            y_extent = ((val * -5.) - 0.75, (val * 5.) + 0.75)
            markup = markuptools.Markup.filled_box(x_extent, y_extent, 1) 
            markup = markuptools.Markup(markup, 'up')
            attach(markup, v_mean[i])
            color = (90 - int(val * 90))
            color = schemetools.SchemeColor('grey{}'.format(color))
            override(v_mean[i]).text_script.color = color
        for i, val in enumerate(chroma_std):
            markup = r"\filled-box #'(0 . 1.25) #'({} . {}) #1".format(
                (val * -5.) - 0.75,
                (val * 5.) + 0.75,
                )
            markup = markuptools.Markup(markup, 'down')
            attach(markup, v_std[i])
            color = (90 - int(val * 90))
            color = schemetools.SchemeColor('grey{}'.format(color))
            override(v_std[i]).text_script.color = color
        override(v_mean).text_script.staff_padding = 1.5
        override(v_std).text_script.staff_padding = 3.0
        override(staff).stem.transparent = True
        staff.remove_commands.append('Time_signature_engraver')
        staff.remove_commands.append('Bar_engraver')
        score = scoretools.Score([staff])
        illustration = score.__illustrate__()
        return illustration

    def _normalize(self, ndarray):
        nda = ndarray - ndarray.min()
        nda = nda / nda.max()
        return nda