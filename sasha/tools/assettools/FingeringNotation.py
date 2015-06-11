from abjad import *
from sasha.tools.domaintools.Fingering import Fingering
from sasha.tools.assettools.Notation import Notation


class FingeringNotation(Notation):

    __domain_class__ = Fingering
    __requires__ = None

    plugin_label = 'fingering'

    ### PRIVATE METHODS ###

    def _make_illustration(self, *args):
        fingering = Fingering.get_one(id=self.client.id)
        key_names = [x.name for x in fingering.instrument_keys]
        markup = self._make_markup(key_names)
        illustration = markup.__illustrate__()
        return illustration

    def _make_markup(self, fingering_definition):
        parts = {
            'cc': [],
            'lh': [],
            'rh': [],
            }
        key_translation = {
            '8va': ('lh', 'T'),
            'B': ('lh', 'b'),
            'Bf': ('lh', 'low-bes'),
            'Bis': ('lh', 'bes'),
            'C': ('rh', 'low-c'),
            'C1': ('lh', 'd'),
            'C2': ('lh', 'ees'),
            'C3': ('rh', 'e'),
            'C4': ('lh', 'f'),
            'C5': ('rh', 'high-fis'),
            # 'C6':   ('rh', 'high-fis'), # doubling C5 ?
            'Cs': ('lh', 'cis'),
            'Ef': ('rh', 'ees'),
            'Gs': ('lh', 'gis'),
            'L1': ('cc', 'one'),
            'L2': ('cc', 'two'),
            'L3': ('cc', 'three'),
            # 'LowA':
            'R1': ('cc', 'four'),
            'R2': ('cc', 'five'),
            'R3': ('cc', 'six'),
            'Ta': ('rh', 'bes'),
            'Tc': ('rh', 'c'),
            'Tf': ('rh', 'fis'),
            'X': ('lh', 'front-f'),
            }
        for english_name in key_translation:
            if english_name in fingering_definition:
                part, name = key_translation[english_name]
                parts[part].append(name)
        for key, value in parts.iteritems():
            parts[key] = schemetools.SchemePair(key, value)
        instrument = 'saxophone'
        user_draw_commands = schemetools.Scheme(parts.values(), quoting="'")
        markup = markuptools.Markup(
            markuptools.MarkupCommand(
                'woodwind-diagram',
                schemetools.Scheme(instrument, quoting="'"),
                user_draw_commands
                ),
            )
        markup = markup.override(('size', 0.5))
        markup = markup.override(('thickness', 0.1))
        markup = markup.scale((1.5, 1.5))
        markup = markup.with_dimensions((-2.5, 2.5), (0, 15))
        markup = markup.scale((1.5, 1.5))
        return markup