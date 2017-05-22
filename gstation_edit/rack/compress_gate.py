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

from ..ui_core.cbx_parameter import *
from ..ui_core.scale_parameter import *
from ..ui_core.btn_parameter import *

from .rack_unit import *

class CompressorGateUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'compressor-gate-unit')

        self._compressor_ratio = CbxParameter(parent=self,
                                              name='compressor-ratio',
                                              parameter_nb=2,
                                              jstation_command=3,
                                              max_value=9)
        self._compressor_freq = CbxParameter(parent=self,
                                             name='compressor-freq',
                                             parameter_nb=4,
                                             jstation_command=5,
                                             max_value=19)
        self._compressor_threshold = ScaleParameter(parent=self,
                                                    name='compressor-threshold',
                                                    parameter_nb=1,
                                                    jstation_command=2,
                                                    max_value=50)
        self._compressor_gain = ScaleParameter(parent=self,
                                               name='compressor-gain',
                                               parameter_nb=3,
                                               jstation_command=4,
                                               max_value=30)
        self._compressor_on_off_btn = BtnParameter(parent=self,
                                                   name='compressor',
                                                   parameter_nb=0,
                                                   jstation_command=1)

        self._gate_threshold = ScaleParameter(parent=self,
                                              name='gate-threshold',
                                              parameter_nb=18,
                                              jstation_command=43,
                                              min_value=1,
                                              max_value=50)
        self._gate_attack = ScaleParameter(parent=self,
                                           name='gate-attack',
                                           parameter_nb=17,
                                           jstation_command=42,
                                           max_value=10)
        self._gate_on_off_btn = BtnParameter(parent=self,
                                             name='gate',
                                             parameter_nb=16,
                                             jstation_command=41)

