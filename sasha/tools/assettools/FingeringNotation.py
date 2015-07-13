import os
from abjad.tools import markuptools
from abjad.tools import schemetools
from sasha.tools.assettools.Notation import Notation


class FingeringNotation(Notation):

    ### CLASS VARIABLES ###

    __requires__ = None
    __slots__ = ()
    asset_label = 'fingering'

    ### PRIVATE METHODS ###

    def _build_path(self):
        from sasha import sasha_configuration
        name = str(self.client.canonical_fingering_name)
        if self.asset_label:
            name += '__{}'.format(self.asset_label)
        if self.file_suffix:
            name += '.{}'.format(self.file_suffix)
        media_path = sasha_configuration.get_media_path(self.media_type)
        build_path = os.path.join(media_path, name)
        return build_path

    def _make_illustration(self, *args):
        fingering = self.client.fingering
        markup = self._make_markup(fingering.key_names)
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
        markup = markup.override(('thickness', 0.15))
        markup = markup.scale((2, 2))
        markup = markup.pad_around(0.25)
        return markup

    ### PUBLIC METHODS ###

    def get_image_link(self, request):
        from webhelpers.html import HTML
        href = self.client.fingering.get_url(request)
        content = self.get_image_tag(request)
        return HTML.tag('a', href=href, c=content)