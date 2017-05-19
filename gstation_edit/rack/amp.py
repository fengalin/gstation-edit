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

from ..ui_core.cbx_parameter import *
from ..ui_core.scale_parameter import *

from .rack_unit import *

class AmpUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'amp-unit')

        self._amp_modeling = CbxParameter(parent=self,
                                          name='amp-model',
                                          parameter_nb=9,
                                          jstation_command=34,
                                          max_value=24)
        self._cabinet = CbxParameter(parent=self,
                                     name='cabinet-type',
                                     parameter_nb=15,
                                     jstation_command=66,
                                     max_value=18)
        self._gain = ScaleParameter(parent=self,
                                    name='gain',
                                    parameter_nb=10,
                                    jstation_command=35,
                                    max_value=90)
        self._treble = ScaleParameter(parent=self,
                                      name='treble',
                                      parameter_nb=11,
                                      jstation_command=39,
                                      max_value=90)
        self._mid = ScaleParameter(parent=self,
                                   name='mid',
                                   parameter_nb=12,
                                   jstation_command=38,
                                   max_value=90)
        self._bass = ScaleParameter(parent=self,
                                    name='bass',
                                    parameter_nb=13,
                                    jstation_command=37,
                                    max_value=90)
        self._level = ScaleParameter(parent=self,
                                     name='level',
                                     parameter_nb=14,
                                     jstation_command=36,
                                     max_value=90)
