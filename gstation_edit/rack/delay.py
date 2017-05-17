"""
 gstation-edit DelayUnit definition
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

from gstation_edit.ui_core.cbx_parameter import *
from gstation_edit.ui_core.scale_parameter import *
from gstation_edit.ui_core.btn_parameter import *

from rack_unit import *

class DelayUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'delay-unit')

        self._delay_type = CbxParameter(parent=self,
                                        name='delay-type',
                                        parameter_nb=27,
                                        jstation_command=53,
                                        max_value=3)
        self._delay_time_course = ScaleParameter(parent=self,
                                                 name='delay-time-course',
                                                 parameter_nb=29,
                                                 jstation_command=55,
                                                 max_value=30)
        self._delay_time_fine = ScaleParameter(parent=self,
                                               name='delay-time-fine',
                                               parameter_nb=30,
                                               jstation_command=56,
                                               max_value=99)
        self._delay_feedback = ScaleParameter(parent=self,
                                              name='delay-feedback',
                                              parameter_nb=31,
                                              jstation_command=57,
                                              max_value=99)
        self._delay_level = ScaleParameter(parent=self,
                                           name='delay-level',
                                           parameter_nb=28,
                                           jstation_command=54,
                                           max_value=99)
        self._delay_on_off_btn = BtnParameter(parent=self,
                                              name='delay',
                                              parameter_nb=26,
                                              jstation_command=52)

