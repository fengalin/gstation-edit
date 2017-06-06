"""
 gstation-edit WhaExpressionUnit definition
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

class WahExpressionUnit(RackUnit):
    def __init__(self, parent):
         RackUnit.__init__(self, parent=parent, name='wah-expression-unit')

         self.dwah_expression_type = CbxParameter(parent=self,
                                                  name='wah-expression-type',
                                                  cc_nb=70,
                                                  parameter_nb=40,
                                                  max_value=3)
         self.wha_heel = ScaleParameter(parent=self,
                                        name='wah-heel',
                                        cc_nb=10,
                                        parameter_nb=7,
                                        max_value=127,
                                        display_percent=True)
         self.wha_toe = ScaleParameter(parent=self,
                                       name='wah-toe',
                                       cc_nb=11,
                                       parameter_nb=8,
                                       max_value=127,
                                       display_percent=True)
         self.pedal_forward = ScaleParameter(parent=self,
                                             name='pedal-forward',
                                             cc_nb=71,
                                             parameter_nb=41,
                                             max_value=127,
                                             display_percent=True)
         self.pedal_back = ScaleParameter(parent=self,
                                          name='pedal-back',
                                          cc_nb=72,
                                          parameter_nb=42,
                                          max_value=127,
                                          display_percent=True)
         self.wah_expression_on_off_btn = BtnParameter(parent=self,
                                                       name='wah-expression',
                                                       cc_nb=8,
                                                       parameter_nb=5)
