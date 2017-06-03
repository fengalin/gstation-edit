"""
 gstation-edit BtnParameter definition
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

class BtnParameter(Parameter):

    def __init__(self, parent, name, cc_nb=-1, parameter_nb=-1,
                 is_sensitive=1, value=0):
         Parameter.__init__(self, parent, name, cc_nb, parameter_nb,
                            is_sensitive, value)

    def get_str_value(self):
        if 0 == self.value:
            return 'off'
        else:
            return 'on'

    def get_cc_value(self):
        if 0 == self.value:
            value = 0
        else:
            value = 127
        return value

    def get_value_from_cc(self, cc_value):
        if 64 > cc_value:
            value = 0
        else:
            value = 1
        return value

    def get_widget_name(self):
        return self.name + '-btn'

    def init_widget(self, gtk_builder):
        Parameter.init_widget(self, gtk_builder)
        if self._widget != None:
            self._widget.set_active(self.value)

    def get_signal_handlers(self):
        signal_radical = 'on_' + self.get_widget_name()
        signal_handlers = {signal_radical+'_toggled': self.handle_toggled}
        return signal_handlers

    def handle_toggled(self, widget):
        if 0 == widget.get_active():
            self.set_value(0)
        else:
            self.set_value(1)

    def update_widget(self):
        if self._widget != None:
            self._widget.set_active(self.value)

