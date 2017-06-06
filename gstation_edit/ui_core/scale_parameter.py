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

from gi.repository import Gtk

from gstation_edit.ui_core.parameter import Parameter

class ScaleParameter(Parameter):

    def __init__(self, parent, name, cc_nb=-1, parameter_nb=-1, is_sensitive=1,
                 value=0, min_value=0, max_value=99, display_percent=False,
                 auto_register=True):
         self.display_percent = display_percent
         Parameter.__init__(self, parent, name, cc_nb, parameter_nb,
                            is_sensitive, value, min_value, max_value,
                            auto_register)

    def get_str_value(self):
        value = self.value
        if self.display_percent:
            value = 100 * value / self.max_value
        return '%02d'%(value)

    def get_widget_name(self):
        return self.name + '-scale'

    def init_widget(self, gtk_builder):
        Parameter.init_widget(self, gtk_builder)
        if self.widget:
            self.widget.set_range(self.min_value, self.max_value)
            self.widget.connect('change_value', self.handle_change_value)

            self.value_lbl = gtk_builder.get_object('%s-value-lbl'%self.name)

    def init_value(self, value, is_cc=False):
        Parameter.init_value(self, value, is_cc)
        if self.value_lbl:
            self.value_lbl.set_text(self.str_value)

    def set_value(self, value):
        Parameter.set_value(self, value)
        self.value_lbl.set_text(self.str_value)

    def handle_change_value(self, widget, scroll_jump, value):
        int_value = int(value)
        if int_value <= self.min_value:
            int_value = self.min_value
        if int_value >= self.max_value:
            int_value = self.max_value
        self.set_value(int_value)
        return False

    def set_max(self, max_value):
        self.max_value = max_value
        self.widget.set_range(self.min_value, self.max_value)

