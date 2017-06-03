"""
 gstation-edit ScaleParameter definition
"""
# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009-2017 <fengalin@free.fr>
#
# gstation-edit is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gstation-edit is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gstation_edit.ui_core.parameter import Parameter

class ScaleParameter(Parameter):

    def __init__(self, parent, name, cc_nb=-1, parameter_nb=-1, is_sensitive=1,
                 value=0, min_value=0, max_value=99, auto_register=True):
         Parameter.__init__(self, parent, name, cc_nb, parameter_nb,
                            is_sensitive, value, min_value, max_value,
                            auto_register)

    def get_str_value(self):
        return ('0' + str(self.value))[-2:]

    def get_widget_name(self):
        return self.name + '-scale'

    def init_widget(self, gtk_builder):
        Parameter.init_widget(self, gtk_builder)
        if self._widget != None:
            self._widget.set_range(self.min_value, self.max_value)

    def get_signal_handlers(self):
        signal_radical = 'on_' + self.get_widget_name()
        signal_handlers = dict()
        signal_handlers[signal_radical+'_change_value'] = self.handle_change_value
        signal_handlers[signal_radical+'_format_value'] = self.handle_format_value
        return signal_handlers

    def handle_change_value(self, widget, scroll_jump, value):
        int_value = int(value)
        if self.min_value<=int_value and self.max_value>=int_value:
            self.set_value(int_value)

    def handle_format_value(self, widget, value):
        return self.str_value

