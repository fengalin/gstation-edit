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

from gstation_edit.ui_core.cbx_parameter import CbxParameter
from gstation_edit.ui_core.scale_parameter import ScaleParameter
from gstation_edit.ui_core.btn_parameter import BtnParameter

from gstation_edit.rack.rack_unit import RackUnit

class DelayUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'delay-unit')

        self.delay_type = CbxParameter(parent=self,
                                       name='delay-type',
                                       cc_nb=53,
                                       parameter_nb=27,
                                       max_value=3)
        self.delay_time_course = ScaleParameter(parent=self,
                                                name='delay-time-course',
                                                cc_nb=55,
                                                parameter_nb=29,
                                                max_value=30)
        self.delay_time_fine = ScaleParameter(parent=self,
                                              name='delay-time-fine',
                                              cc_nb=56,
                                              parameter_nb=30,
                                              min_value=1,
                                              max_value=99)
        self.delay_feedback = ScaleParameter(parent=self,
                                             name='delay-feedback',
                                             cc_nb=57,
                                             parameter_nb=31,
                                             max_value=99)
        self.delay_level = ScaleParameter(parent=self,
                                          name='delay-level',
                                          cc_nb=54,
                                          parameter_nb=28,
                                          max_value=99,
                                          display_percent=True)
        self.delay_on_off_btn = BtnParameter(parent=self,
                                             name='delay',
                                             cc_nb=52,
                                             parameter_nb=26)
