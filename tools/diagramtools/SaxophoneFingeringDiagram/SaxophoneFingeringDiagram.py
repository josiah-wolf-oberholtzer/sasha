from abjad.tools.markuptools import MarkupCommand
from abjad.tools.schemetools import SchemePair
from sasha.tools.diagramtools._Diagram import _Diagram


class SaxophoneFingeringDiagram(_Diagram):

    fontsize = 7
    radius = 0.75
    thickness = 0.2

    def __call__(self, definition):
        funcdict = {
            '8va': self._build_8va,
            'B': self._build_B,
            'Bf': self._build_Bf,
            'Bis': self._build_Bis,
            'C': self._build_C,
            'C1': self._build_C1,
            'C2': self._build_C2,
            'C3': self._build_C3,
            'C4': self._build_C4,
            'C5': self._build_C5,
            'C6': self._build_C6,
            'Cs': self._build_Cs,
            'Ef': self._build_Ef,
            'Gs': self._build_Gs,
            'L1': self._build_L1,
            'L2': self._build_L2,
            'L3': self._build_L3,
            'LowA': self._build_LowA,
            'R1': self._build_R1,
            'R2': self._build_R2,
            'R3': self._build_R3,
            'Ta': self._build_Ta,
            'Tc': self._build_Tc,
            'Tf': self._build_Tf,
            'X': self._build_X,
        }
        elements = [ ]
        for key in funcdict.keys( ):
            result = funcdict[key](key in definition)
            if result is not None:
                elements.append(result)
        elements.append(self._build_common( ))
        return self._combine_markup_commands(elements)

    ### PRIVATE METHODS

    def _build_8va(self, state):
        if state:
            m = '8va'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 0, 11)
            return m
        return None

    def _build_B(self, state):
        if state:
            m = 'B'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 4.5, 2)
            return m
        return None

    def _build_Bf(self, state):
        if state:
            m_a = 'B'
            m_b = MarkupCommand('flat', None, None)
            m_a = self._center_markup_command_vertically(m_a)
            m_b = self._center_markup_command_vertically(m_b)
            m = self._put_markup_commands_adjacent(m_a, m_b, 'X', 'RIGHT')
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 3, 1)
            return m
        return None

    def _build_Bis(self, state):
        if state:
            m = self._draw_circle(0.75 * self.radius, self.thickness, True)
            m = self._translate_markup_command(m, 1.5, 4.5)
            return m
        return None

    def _build_C(self, state):
        if state:
            m = 'C'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 0, -9)
            return m
        return None

    def _build_C1(self, state):
        if state:
            m = 'C1'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -3, 5)
            return m
        return None

    def _build_C2(self, state):
        if state:
            m = 'C2'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -1.5, 6)
            return m
        return None

    def _build_C3(self, state):
        if state:
            m = 'C3'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -3, 1)
            return m
        return None

    def _build_C4(self, state):
        if state:
            m = 'C4'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -1.5, 4)
            return m
        return None

    def _build_C5(self, state):
        if state:
            m = 'C5'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -1.5, -2)
            return m
        return None

    def _build_C6(self, state):
        if state:
            m = 'C6'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -1.5, -4)
            return m
        return None
    
    def _build_Cs(self, state):
        if state:
            m_a = 'C'
            m_b = MarkupCommand('sharp', None, None)
            m_a = self._center_markup_command_vertically(m_a)
            m_b = self._center_markup_command_vertically(m_b)
            m = self._put_markup_commands_adjacent(m_a, m_b, 'X', 'RIGHT')
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 1.5, 2)
            return m
        return None

    def _build_Ef(self, state):
        if state:
            m_a = 'E'
            m_b = MarkupCommand('flat', None, None)
            m_a = self._center_markup_command_vertically(m_a)
            m_b = self._center_markup_command_vertically(m_b)
            m = self._put_markup_commands_adjacent(m_a, m_b, 'X', 'RIGHT')
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 0, -7)
            return m
        return None

    def _build_Gs(self, state):
        if state:
            m_a = 'G'
            m_b = MarkupCommand('sharp', None, None)
            m_a = self._center_markup_command_vertically(m_a)
            m_b = self._center_markup_command_vertically(m_b)
            m = self._put_markup_commands_adjacent(m_a, m_b, 'X', 'RIGHT')
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 1.5, 4)
            return m
        return None

    def _build_L1(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, 5)
        return m

    def _build_L2(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, 3)
        return m

    def _build_L3(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, 1)
        return m

    def _build_LowA(self, state):
        if state:
            m = 'LowA'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 0, 9)
            return m
        return None

    def _build_R1(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, -1)
        return m

    def _build_R2(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, -3)
        return m

    def _build_R3(self, state):
        if state:
            m = self._draw_circle(self.radius, self.thickness, True)
        else:
            m = self._draw_circle(self.radius, self.thickness, False)
        m = self._translate_markup_command(m, 0, -5)
        return m

    def _build_Ta(self, state):
        if state:
            m = 'Ta'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -3, -5)
            return m
        return None

    def _build_Tc(self, state):
        if state:
            m = 'Tc'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -3, -3)
            return m
        return None

    def _build_Tf(self, state):
        if state:
            m = 'Tf'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, -1.5, -6)
            return m
        return None

    def _build_X(self, state):
        if state:
            m = 'X'
            m = self._format_text_markup(m, self.fontsize)
            m = self._center_markup_command_bidirectionally(m)
            m = self._translate_markup_command(m, 0, 7)
            return m
        return None

    def _build_common(self):
        m = MarkupCommand('draw-line', [SchemePair(2, 0)], None)
        m = self._center_markup_command_bidirectionally(m)
        return m
