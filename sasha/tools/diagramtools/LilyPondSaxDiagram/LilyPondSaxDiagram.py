from abjad.tools import markuptools
from abjad.tools import schemetools


class LilyPondSaxDiagram(object):

    def __call__(self, fingering_definition):

        parts = {
            'cc': [],
            'lh': [],
            'rh': [],
        }

        key_translation = {
            '8va':  ('lh', 'T'),
            'B':    ('lh', 'b'),
            'Bf':   ('lh', 'low-bes'),
            'Bis':  ('lh', 'bes'),
            'C':    ('rh', 'low-c'),
            'C1':   ('lh', 'd'),
            'C2':   ('lh', 'ees'),
            'C3':   ('rh', 'e'),
            'C4':   ('lh', 'f'),
            'C5':   ('rh', 'high-fis'),
#            'C6':   ('rh', 'high-fis'), # doubling C5 ?
            'Cs':   ('lh', 'cis'),
            'Ef':   ('rh', 'ees'),
            'Gs':   ('lh', 'gis'),
            'L1':   ('cc', 'one'),
            'L2':   ('cc', 'two'),
            'L3':   ('cc', 'three'),
#            'LowA':  
            'R1':   ('cc', 'four'),
            'R2':   ('cc', 'five'),
            'R3':   ('cc', 'six'),
            'Ta':   ('rh', 'bes'),
            'Tc':   ('rh', 'c'),
            'Tf':   ('rh', 'fis'),
            'X':    ('lh', 'front-f'),
        }

        for english_name in key_translation:
            if english_name in fingering_definition:
                part, name = key_translation[english_name]
                parts[part].append(name)

        for key, value in parts.iteritems():
            #parts[key] = '(%s . (%s))' % (key, ' '.join(value))
            parts[key] = schemetools.SchemePair(key, value)

        instrument = 'saxophone'
        user_draw_commands = schemetools.Scheme(parts.values(), quoting="'")

        diagram = markuptools.MarkupCommand(
            'woodwind-diagram',
            schemetools.Scheme(instrument, quoting="'"),
            user_draw_commands
            )

        diagram = markuptools.MarkupCommand(
            'override', 
            schemetools.SchemePair('size', 0.5), 
            diagram
            )

        diagram = markuptools.MarkupCommand(
            'override', 
            schemetools.SchemePair('thickness', 0.1), 
            diagram
            )

        diagram = markuptools.MarkupCommand(
            'scale', 
            schemetools.SchemePair(1.5, 1.5), 
            diagram
            )

        diagram = markuptools.MarkupCommand(
            'with-dimensions', 
            schemetools.SchemePair(-2.5, 2.5), 
            schemetools.SchemePair(0, 15), 
            diagram
            )

        return diagram


        
