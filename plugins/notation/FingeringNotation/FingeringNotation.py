from abjad import *
from sasha import *
from sasha.plugins.notation._Notation import _Notation
from sasha.plugins.analysis import ChordAnalysis
from sasha.tools.diagramtools import LilyPondSaxDiagram


class FingeringNotation(_Notation):

    __client_class__ = Fingering
    __requires__ = None

    plugin_label = 'fingering'

    ### PRIVATE METHODS ###

    def _build_lily(self, *args):
        fingering = Fingering.get_one(id=self.client.fingering_id)
        key_names = [x.name for x in fingering.instrument_keys]
        diagram = LilyPondSaxDiagram()(key_names)
        diagram = markuptools.MarkupCommand('scale', schemetools.SchemePair(1.5, 1.5), diagram)
        markup = markuptools.Markup(diagram)
        lily = lilypondfiletools.make_basic_lilypond_file()
        lily.append(markup)
        return lily

