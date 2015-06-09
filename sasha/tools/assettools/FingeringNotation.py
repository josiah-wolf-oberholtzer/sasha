from abjad import *
from sasha.tools.domaintools.Fingering import Fingering
from sasha.tools.assettools.Notation import Notation
from sasha.tools.diagramtools import LilyPondSaxDiagram


class FingeringNotation(Notation):

    __client_class__ = Fingering
    __requires__ = None

    plugin_label = 'fingering'

    ### PRIVATE METHODS ###

    def _build_lily(self, *args):
        fingering = Fingering.get_one(id=self.client.id)
        key_names = [x.name for x in fingering.instrument_keys]
        diagram = LilyPondSaxDiagram()(key_names)
        diagram = markuptools.MarkupCommand('scale', schemetools.SchemePair(1.5, 1.5), diagram)
        markup = markuptools.Markup(diagram)
        illustration = markup.__illustrate__()
        return illustration