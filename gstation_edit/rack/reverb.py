"""
 gstation-edit ReverbUnit definition
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
from ..ui_core.btn_parameter import BtnParameter

from .rack_unit import RackUnit

class ReverbUnit(RackUnit):
    def __init__(self, parent):
         RackUnit.__init__(self, parent, 'reverb-unit')

         self._reverb_type = CbxParameter(parent=self,
                                          name='reverb-type',
                                          cc_nb=60,
                                          parameter_nb=33,
                                          max_value=12)
         self._reverb_diffusion = ScaleParameter(parent=self,
                                                 name='reverb-diffusion',
                                                 cc_nb=62,
                                                 parameter_nb=35,
                                                 max_value=99)
         self._reverb_density = ScaleParameter(parent=self,
                                               name='reverb-density',
                                               cc_nb=63,
                                               parameter_nb=36,
                                               max_value=99)
         self._reverb_decay = ScaleParameter(parent=self,
                                             name='reverb-decay',
                                             cc_nb=65,
                                             parameter_nb=37,
                                             max_value=9)
         self._reverb_level = ScaleParameter(parent=self,
                                             name='reverb-level',
                                             cc_nb=61,
                                             parameter_nb=34,
                                             max_value=99)
         self._reverb_on_off_btn = BtnParameter(parent=self,
                                                name='reverb',
                                                cc_nb=59,
                                                parameter_nb=32)


    def update_conf_from_parameter(self, parameter):
        if parameter == self._reverb_type:
            str_value = parameter.str_value
            sensitivity = True
            if str_value == '2-Spring 7\"' or \
                    str_value == '2-Spring 14\"' or \
                    str_value == '3-Spring 14\"' or \
                    str_value == 'Rattle \'n\' Boing':
                sensitivity = False

            self._reverb_diffusion.set_sensitive(sensitivity)
            self._reverb_density.set_sensitive(sensitivity)
            self._reverb_decay.set_sensitive(sensitivity)

