"""
 gstation-edit UtilitiesDlg definition
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


from gstation_edit.ui_core.scale_parameter import ScaleParameter

from gstation_edit.messages.utility_settings_resp import UtilitySettingsResponse

# Note: might be an heir of RackUnit because of the scale parameter
# Or RackUnit could inherit a ParameterCollection or something similar
# of UtilitiesDlg would inherit ParameterCollection
class UtilitiesDlg:
    def __init__(self, main_window, gtk_builder):
        self.main_window = main_window
        self.gtk_builder = gtk_builder

        self.settings = UtilitySettingsResponse()

        self.prevent_propagation = False

        self.gtk_dlg = self.get_widget('utilities-dlg')
        self.done_btn = self.get_widget('utilities-done-btn')

        self.cabinet_emul_switch = self.get_widget('cabinet-emulation-swtch')
        self.stereo_switch = self.get_widget('stereo-swtch')
        self.dry_track_switch = self.get_widget('dry-track-swtch')
        self.midi_loopback_switch = self.get_widget('midi-loopback-swtch')

        # digital level is the only utility parameter
        # to be associated to a CC parameter
        self.digital_level = self.get_widget('digital-level-scale')
        self.digital_level_scale = ScaleParameter(parent=self,
                                                  name='digital-level',
                                                  cc_nb=14,
                                                  max_value=24,
                                                  auto_register=False)
        self.digital_level_scale.init_widget(self.gtk_builder)
        self.digital_level_radical = 'on_digital-level-scale'
        self.digital_level_regular_callback = \
            self.digital_level_scale.get_signal_handlers()[
                self.digital_level_radical + '_change_value'
            ]
        self.digital_level_has_changed = False


    def get_widget(self, widget_name):
        widget = self.gtk_builder.get_object(widget_name)
        if widget == None:
            self.is_valid = False
            print('Could not find widget %s'%(widget_name))
        return widget


    def get_signal_handlers(self):
        signal_handlers = dict()
        signal_handlers['on_utilities-done-btn_clicked'] = self.on_done_btn_clicked

        signal_handlers['on_cabinet-emulation-swtch_state_set'] = \
                                                        self.on_utility_changed
        signal_handlers['on_stereo-swtch_state_set'] = \
                                                        self.on_utility_changed
        signal_handlers['on_dry-track-swtch_state_set'] = \
                                                        self.on_utility_changed
        signal_handlers['on_midi-loopback-swtch_state_set'] = \
                                                        self.on_utility_changed

        signal_handlers[self.digital_level_radical + '_change_value'] = \
                                                  self.on_digital_level_changed
        signal_handlers[self.digital_level_radical + '_format_value'] = \
                                   self.digital_level_scale.handle_format_value
        return signal_handlers

    def get_parameter_cc_bindings(self):
        return self.digital_level_scale.get_parameter_cc_bindings()

    def present(self, widget=None):
        self.gtk_dlg.present()

    def update_conf_from_parameter(self, parameter):
        pass

    def send_parameter_value(self, parameter):
        self.main_window.send_parameter_value(parameter,
                                              program_has_changed=False)

    def set_utilities(self, settings_resp):
        self.settings = settings_resp

        self.prevent_propagation = True
        self.cabinet_emul_switch.set_active(self.settings.global_cabinet)
        self.stereo_switch.set_active(self.settings.stereo_mono)
        self.digital_level_scale.init_value(self.settings.digital_out_level)
        self.dry_track_switch.set_active(self.settings.dry_track)
        self.midi_loopback_switch.set_active(self.settings.midi_merge)
        self.prevent_propagation = False


    def on_done_btn_clicked(self, widget):
        if self.digital_level_has_changed:
            # digital out sends the value to the J-Station using CC events
            # however, it needs to be confirmed in order to persist
            self.main_window.send_settings(self.settings)
            self.digital_level_has_changed = False

        self.gtk_dlg.hide()

    def on_digital_level_changed(self, widget, step, value):
        if not self.prevent_propagation:
            self.digital_level_has_changed = True
            self.settings.digital_out_level = int(value)
        self.digital_level_regular_callback(widget, step, value)

    def on_utility_changed(self, widget, value=None):
        if not self.prevent_propagation:
            if widget == self.cabinet_emul_switch:
                self.settings.global_cabinet = value
            elif widget == self.stereo_switch:
                self.settings.stereo_mono = value
            elif widget == self.dry_track_switch:
                self.settings.dry_track = value
            elif widget == self.midi_loopback_switch:
                self.settings.midi_merge = value

            self.main_window.send_settings(self.settings)


