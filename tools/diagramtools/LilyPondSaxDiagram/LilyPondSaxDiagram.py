from abjad.tools.markuptools import MarkupCommand
from abjad.tools.schemetools import SchemePair


class LilyPondSaxDiagram(object):

    def __call__(self, fingering_definition):

        size = 0.5
        thickness = 0.1

        parts = {
            'cc': [ ],
            'lh': [ ],
            'rh': [ ],
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

        for key, value in parts.iteritems( ):
            parts[key] = '(%s . (%s))' % (key, ' '.join(value))

        instrument = "#'saxophone"
        user_draw_commands = "#'(%s)" % ' '.join([x for x in parts.values( )])
        size = "#'(size . %f)" % size
        thickness = "#'(thickness . %f)" % thickness

        diagram = MarkupCommand('woodwind-diagram', [instrument, user_draw_commands], None)
        diagram = MarkupCommand('override', [size], [diagram])
        diagram = MarkupCommand('override', [thickness], [diagram])
        diagram = MarkupCommand('scale', [SchemePair(1.5, 1.5)], [diagram])
        diagram = MarkupCommand('with-dimensions', [SchemePair(-2.5, 2.5), SchemePair(0, 15)], [diagram])
#        diagram = MarkupCommand('rounded-box', None, [diagram])

        return diagram


        
