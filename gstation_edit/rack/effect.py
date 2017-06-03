"""
 gstation-edit EffectUnit definition
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
# with this program.    If not, see <http://www.gnu.org/licenses/>.

from gstation_edit.ui_core.cbx_parameter import CbxParameter
from gstation_edit.ui_core.scale_parameter import ScaleParameter
from gstation_edit.ui_core.btn_parameter import BtnParameter
from gstation_edit.ui_core.rdbtn_parameter import RdBtnParameter
from gstation_edit.ui_core.grp_parameter import GrpParameter

from gstation_edit.rack.rack_unit import RackUnit

class EffectUnit(RackUnit):
    def __init__(self, parent):
        RackUnit.__init__(self, parent, 'effect-unit')

        self._effect_type = CbxParameter(parent=self,
                                         name='effect-type',
                                         cc_nb=45,
                                         parameter_nb=20,
                                         max_value=6)
        self._speed = ScaleParameter(parent=self,
                                     name='effect-speed',
                                     cc_nb=47,
                                     parameter_nb=22,
                                     max_value=90)
        self._depth = ScaleParameter(parent=self,
                                     name='effect-depth',
                                     cc_nb=48,
                                     parameter_nb=23,
                                     max_value=90)
        self._option = ScaleParameter(parent=self,
                                      name='effect-option',
                                      cc_nb=49, # regen
                                      parameter_nb=24,
                                      max_value=90)
        self._mix = ScaleParameter(parent=self,
                                   name='effect-mix',
                                   cc_nb=46, # level
                                   parameter_nb=21,
                                   max_value=90)
        self._on_off_btn = BtnParameter(parent=self,
                                        name='effect',
                                        cc_nb=44, # On/Bypass
                                        parameter_nb=19)

        self._rd_btn_grp = GrpParameter(parent=self, name='effect-rd-btn-grp')
        self._pre_rdbtn = RdBtnParameter(parent=self._rd_btn_grp,
                                         name='effect-pre',
                                         is_active=1,
                                         value=99,
                                         cc_nb=50, # position
                                         parameter_nb=25)
        self._post_rdbtn = RdBtnParameter(parent=self._rd_btn_grp,
                                          name='effect-post',
                                          is_active=0,
                                          value=0,
                                          cc_nb=50, # position
                                          parameter_nb=25)

    # TODO: set option / sensitivity for pitch/detune


    def update_conf_from_parameter(self, parameter):
        if parameter == self._effect_type:
            str_value = parameter.str_value
            option_sensitivity = True
            speed_label = 'Speed:'
            depth_label = 'Depth:'
            option_label = 'PreDelay:'
            if str_value == 'Flanger':
                option_label = 'Regen:'
            elif str_value == 'Tremolo' or str_value == 'Rotary Speaker':
                option_sensitivity = False
            elif str_value == 'Pitch / Detune':
                option_sensitivity = False
                speed_label = 'Pitch:'
                depth_label = 'Detune:'

            self._speed.set_widget_label(speed_label)
            self._depth.set_widget_label(depth_label)
            self._option.set_widget_label(option_label)
            self._option.set_sensitive(option_sensitivity)

