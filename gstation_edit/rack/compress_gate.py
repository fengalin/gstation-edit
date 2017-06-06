"""
 gstation-edit CompressorGateUnit definition
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

class CompressorGateUnit(RackUnit):

    class ThresholdScaleParameter(ScaleParameter):
        def get_str_value(self):
            # e.g. 0 => -50dB, 50: 0dB
            return '%d'%(self.value - self.max_value)

    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'compressor-gate-unit')

        self.compressor_ratio = CbxParameter(parent=self,
                                             name='compressor-ratio',
                                             cc_nb=3,
                                             parameter_nb=2,
                                             max_value=9)
        self.compressor_freq = CbxParameter(parent=self,
                                            name='compressor-freq',
                                            cc_nb=5,
                                            parameter_nb=4,
                                            max_value=19)
        self.compressor_gain = ScaleParameter(parent=self,
                                              name='compressor-gain',
                                              cc_nb=4,
                                              parameter_nb=3,
                                              max_value=30)
        self.compressor_threshold = CompressorGateUnit.ThresholdScaleParameter(
                                                    parent=self,
                                                    name='compressor-threshold',
                                                    cc_nb=2,
                                                    parameter_nb=1,
                                                    max_value=50)
        self.compressor_on_off_btn = BtnParameter(parent=self,
                                                  name='compressor',
                                                  cc_nb=1,
                                                  parameter_nb=0)
        self.gate_threshold = ScaleParameter(parent=self,
                                             name='gate-threshold',
                                             cc_nb=43,
                                             parameter_nb=18,
                                             min_value=1,
                                             max_value=99,
                                             display_percent=True)
        self.gate_attack = ScaleParameter(parent=self,
                                          name='gate-attack',
                                          cc_nb=42,
                                          parameter_nb=17,
                                          max_value=10)
        self.gate_on_off_btn = BtnParameter(parent=self,
                                            name='gate',
                                            cc_nb=41,
                                            parameter_nb=16)
