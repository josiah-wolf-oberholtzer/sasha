from sasha.plugins.notation._Notation import _Notation
from sasha.tools.diagramtools import SaxophoneFingeringDiagram


class IdiomNotation(_Notation):

    _label = 'idiom'

    ### PRIVATE METHODS ###

    def _build_lily(self, sublabel = None):
        from abjad.tools.lilypondfiletools import make_basic_lilypond_file
        from abjad.tools.markuptools import Markup

        idiom = self.event.idiom.idiom
        diagram = SaxophoneFingeringDiagram( )(idiom)
        lily = make_basic_lilypond_file( )
        lily.score_block.append(Markup(diagram))

        return lily
