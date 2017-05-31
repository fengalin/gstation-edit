"""
 gstation-edit Parameter definition
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

class Parameter:
    def __init__(self, parent, name, cc_nb=-1, parameter_nb=-1,
                 is_sensitive=1, value=0, min_value=0, max_value=99,
                 auto_register=True):
        self._parent = parent
        self._widget = None
        self._widget_label = None
        self.name = name
        self.parameter_nb = parameter_nb
        self.cc_nb = cc_nb
        self.is_sensitive = is_sensitive
        self.value = value
        self.str_value = self.get_str_value()
        self.min_value = min_value
        self.max_value = max_value
        if auto_register:
            parent.add_parameter(self)

    def set_value(self, value):
        if self.value != value:
            self.value = value
            self.str_value = self.get_str_value()
            self._parent.update_conf_from_parameter(self)
            self._parent.send_parameter_value(self)

    def init_value(self, value, is_cc=False):
        actual_value = value
        if is_cc:
            actual_value = self.get_value_from_cc(value)
        if self.value != actual_value:
            self.value = actual_value
            self.update_widget()
            self.str_value = self.get_str_value()
            self._parent.update_conf_from_parameter(self)

    def get_str_value(self):
        return str(self.value)

    def get_cc_value(self):
        return int(round(127.0 * self.value / self.max_value))

    def get_value_from_cc(self, cc_value):
        return int(round(cc_value * self.max_value / 127.0))

    def get_widget_name(self):
        return 'not defined'

    def get_widget_label_name(self):
        return self.name + '-lbl'

    def get_signal_handlers(self):
        pass

    def get_parameter_bindings(self):
        result = dict()
        if self.parameter_nb != -1:
            result[self.parameter_nb] = self
        return result

    def get_parameter_cc_bindings(self):
        result = dict()
        if self.cc_nb != -1:
            result[self.cc_nb] = self
        return result

    def init_widget(self, gtk_builder):
        widget_label = gtk_builder.get_object(self.get_widget_label_name())
        if widget_label != None:
            self._widget_label = widget_label

        widget = gtk_builder.get_object(self.get_widget_name())
        if widget != None:
            self._widget = widget
        else:
            print('widget not found: %s'%(self.get_widget_name()))


    def set_widget_label(self, widget_name):
        if self._widget_label != None:
            self._widget_label.set_text(widget_name)

    def set_sensitive(self, is_sensitive):
        self.is_sensitive = is_sensitive
        self._widget.set_sensitive(is_sensitive)
        if self._widget_label != None:
            self._widget_label.set_sensitive(is_sensitive)

    def update_widget(self):
        if self._widget != None:
            self._widget.set_value(self.value)

    def __str__(self):
        return "%s: value %d, in [ %d, %d] - param %d, cc nb %d"\
                %(self.name, self.value, self.min_value, self.max_value,
                 self.parameter_nb, self.cc_nb)

