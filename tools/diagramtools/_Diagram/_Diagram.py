import math
from abjad.tools.markuptools import MarkupCommand
from abjad.tools.schemetools import SchemeBoolean
from abjad.tools.schemetools import SchemeColor
from abjad.tools.schemetools import SchemeNumber
from abjad.tools.schemetools import SchemePair
from abjad.tools.schemetools import SchemeVariable


class _Diagram(object):

    ### PRIVATE METHODS

    def _cartopol(self, x, y, degrees = True):
        if degrees:
            return math.hypot(x, y), 180.0 * math.atan2(y, x) / math.pi
        else:
            return math.hypot(x, y), math.atan2(y, x)

    def _center_markup_command_bidirectionally(self, markup_command):
        m = self._center_markup_command_horizontally(markup_command)
        m = self._center_markup_command_vertically(m)
        return m

    def _center_markup_command_horizontally(self, markup_command):
        return MarkupCommand('center-align', None, [markup_command])

    def _center_markup_command_vertically(self, markup_command):
        return MarkupCommand('vcenter', None, [markup_command])

    def _color_markup_command(self, markup_command, color_string):
        return MarkupCommand('with-color', [SchemeColor(color_string)], [markup_command])

    def _combine_markup_commands(self, markup_commands):
        assert len(markup_commands)
        if len(markup_commands) == 1:
            combined = markup_commands[0]
        else:
            combined = MarkupCommand('combine', None, markup_commands[:2], is_braced = False)
            for markup_command in markup_commands[2:]:
                combined = MarkupCommand('combine', None, [combined, markup_command], is_braced = False)
        return combined

    def _draw_circle(self, radius, line_width, filled):
        return MarkupCommand('draw-circle',
            [SchemeNumber(radius), SchemeNumber(line_width), SchemeBoolean(filled)], None)

    def _format_text_markup(self, markup, fontsize):
        m = MarkupCommand('bold', None, [markup])
        m = MarkupCommand('abs-fontsize', [SchemeNumber(fontsize)], [m])
        m = MarkupCommand('normal-text', None, [m])
        return m

    def _poltocar(self, r, w, degrees = True):
        if degrees:
            w = math.pi * w / 180.0
        return r * math.cos(w), r * math.sin(w)

    def _put_markup_commands_adjacent(self, command_one, command_two, axis, direction):
        return MarkupCommand('put-adjacent',
            [SchemeVariable(axis), SchemeVariable(direction)], [command_one, command_two], is_braced = False)

    def _rotate_markup_command(self, markup_command, w):
        return MarkupCommand('rotate', [SchemeNumber(w)], [markup_command])

    def _scale_markup_command(self, markup_command, x, y):
        return MarkupCommand('scale', [SchemePair(x, y)], [markup_command])

    def _translate_markup_command(self, markup_command, x, y):
        return MarkupCommand('translate', [SchemePair(x, y)], [markup_command])
