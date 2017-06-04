"""
 gstation-edit RdBtnParameter definition
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

from gstation_edit.ui_core.btn_parameter import BtnParameter

class RdBtnParameter(BtnParameter):
    def __init__(self, parent, name, cc_nb=-1, parameter_nb=-1,
                 is_sensitive=1, is_active=1, value=0):
        self.is_active = is_active
        BtnParameter.__init__(self, parent, name, cc_nb, parameter_nb,
                              is_sensitive, value)

    def get_str_value(self):
        if self.is_active == 0:
            return ''
        else:
            return str(self.value)

    def get_widget_name(self):
        return self.name + '-rdbtn'

    def handle_toggled(self, widget):
        self.is_active = widget.get_active()
        if self.is_active != 0:
            self._parent.send_parameter_value(self)

    def set_active(self, is_active):
        if self._widget:
            self._widget.set_active(is_active)

