"""
 gstation-edit RackUnit definition
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

from ..ui_core.parameter import Parameter

class RackUnit:
    def __init__(self, parent, name):
        self._parameters = dict()
        self.parent = parent
        self.name = name

    def add_parameter(self, parameter):
        self._parameters[parameter.name] = parameter

    def init_widgets(self, gtk_builder):
        for parameter in self._parameters.values():
            parameter.init_widget(gtk_builder)

    def get_signal_handlers(self):
        signal_handlers = dict()
        for parameter in self._parameters.values():
            signal_handlers.update(parameter.get_signal_handlers())
        return signal_handlers

    def get_parameter_bindings(self):
        parameter_bindings = dict()
        for parameter in self._parameters.values():
            parameter_bindings.update(parameter.get_parameter_bindings())
        return parameter_bindings

    def get_parameter_cc_bindings(self):
        parameter_cc_bindings = dict()
        for parameter in self._parameters.values():
            parameter_cc_bindings.update(parameter.get_parameter_cc_bindings())
        return parameter_cc_bindings

    def update_conf_from_parameter(self, parameter):
        pass

    def send_parameter_value(self, parameter):
        self.parent.send_parameter_value(parameter)

    def __str__( self ):
        parameters_str = ''
        for parameter in self._parameters.values():
            parameters_str += parameter
        return "Rack unit: %s%s"%(self.name, parameters_str)
