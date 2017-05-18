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

from ..ui_core.cbx_parameter import *
from ..ui_core.scale_parameter import *
from ..ui_core.btn_parameter import *

from .rack_unit import *

class WhaExpressionUnit(RackUnit):
    def __init__(self, parent):
         RackUnit.__init__(self, parent=parent, name='wah-expression-unit')

         self.dwah_expression_type = CbxParameter(parent=self,
                                                  name='wah-expression-type',
                                                  parameter_nb=40,
                                                  jstation_command=70,
                                                  max_value=3)
         self.wha_heel = ScaleParameter(parent=self,
                                        name='wha-heel',
                                        parameter_nb=7,
                                        jstation_command=10)
         self.wha_toe = ScaleParameter(parent=self,
                                       name='wha-toe',
                                       parameter_nb=8,
                                       jstation_command=11)
         self.pedal_forward = ScaleParameter(parent=self,
                                             name='pedal-forward',
                                             parameter_nb=41,
                                             jstation_command=71)
         self.pedal_back = ScaleParameter(parent=self,
                                          name='pedal-back',
                                          parameter_nb=42,
                                          jstation_command=72)
         self.wah_expression_on_off_btn = BtnParameter(parent=self,
                                                       name='wah-expression',
                                                       parameter_nb=5,
                                                       jstation_command=8)

