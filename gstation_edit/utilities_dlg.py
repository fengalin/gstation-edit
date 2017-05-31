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


from .ui_core.scale_parameter import ScaleParameter

from .messages.utility_settings_resp import UtilitySettingsResponse

class UtilitiesDlg:
    def __init__(self, main_window, js_interface, gtk_builder):
        self.main_window = main_window
        self.js_interface = js_interface
        self.gtk_builder = gtk_builder

        self.settings = UtilitySettingsResponse()

        self.gtk_dlg = self.get_widget('utilities-dlg')
        self.done_btn = self.get_widget('utilities-done-btn')

        self.cabinet_emul_switch = self.get_widget('cabinet-emulation-swtch')
        self.stereo_switch = self.get_widget('stereo-swtch')
        self.dry_track_switch = self.get_widget('dry-track-swtch')
        self.midi_loopback_switch = self.get_widget('midi-loopback-swtch')
        self.midi_channel_spbtn = self.get_widget('utilities-midi-channel-spbtn')

        # digital level is the only utility parameter
        # to be associated to a CC parameter
        self.digital_level = self.get_widget('digital-level-scale')
        # TODO: update max value
        #self._gain = ScaleParameter(parent=self,
        #                            name='digital-level',
        #                            cc_nb=14,
        #                            max_value=90,
        #                            auto_register=False)


    def get_widget(self, widget_name):
        widget = self.gtk_builder.get_object(widget_name)
        if None == widget:
            self.is_valid = False
            print('Could not find widget %s'%(widget_name))
        return widget


    def get_signal_handlers(self):
        signal_handlers = dict()
        signal_handlers['on_utilities-done-btn_clicked'] = self.on_done_btn_clicked
        # TODO: connect handles for on_utility_changed
        # TODO: link digital_level to appropriate CC event (check what J-Edit does)
        return signal_handlers


    def present(self, widget=None):
        self.gtk_dlg.present()

    def set_utilities(self, settings_resp):
        self.settings = settings_resp

        # TODO: figure out how to present
        # change propagation
        # see what is done when CC events are received
        self.stereo_switch.set_active(self.settings.stereo_mono)
        self.dry_track_switch.set_active(self.settings.dry_track)
        self.digital_level.set_value(self.settings.digital_out_level)
        self.cabinet_emul_switch.set_active(self.settings.global_cabinet)
        self.midi_loopback_switch.set_active(self.settings.midi_merge)
        self.midi_channel_spbtn.set_value(self.settings.midi_channel)


    def on_done_btn_clicked(self, widget):
        self.gtk_dlg.hide()

    def on_utility_changed(self, widget):
        # send update to J-Station
        pass


