"""
 gstation-edit AmpUnit definition
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

from ..ui_core.cbx_parameter import CbxParameter
from ..ui_core.scale_parameter import ScaleParameter

from .rack_unit import RackUnit

class AmpUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'amp-unit')

        self._amp_modeling = CbxParameter(parent=self,
                                          name='amp-model',
                                          cc_nb=34,
                                          parameter_nb=9,
                                          max_value=24)
        self._cabinet = CbxParameter(parent=self,
                                     name='cabinet-type',
                                     cc_nb=66,
                                     parameter_nb=15,
                                     max_value=18)
        self._gain = ScaleParameter(parent=self,
                                    name='gain',
                                    cc_nb=35,
                                    parameter_nb=10,
                                    max_value=90)
        self._treble = ScaleParameter(parent=self,
                                      name='treble',
                                      cc_nb=39,
                                      parameter_nb=11,
                                      max_value=90)
        self._mid = ScaleParameter(parent=self,
                                   name='mid',
                                   cc_nb=38,
                                   parameter_nb=12,
                                   max_value=90)
        self._bass = ScaleParameter(parent=self,
                                    name='bass',
                                    cc_nb=37,
                                    parameter_nb=13,
                                    max_value=90)
        self._level = ScaleParameter(parent=self,
                                     name='level',
                                     cc_nb=36,
                                     parameter_nb=14,
                                     max_value=90)
