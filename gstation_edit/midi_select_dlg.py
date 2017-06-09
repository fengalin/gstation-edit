"""
 gstation-edit MidiSelectDlg definition
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

from gi.repository import Gtk
from threading import Thread


class MidiSelectDlg:
    def __init__(self, gtk_builder, main_window, js_interface,
                 on_connected, on_close=None):
        self.main_window = main_window
        self.on_connected = on_connected
        self.on_close = on_close

        self.js_interface = js_interface
        self.gtk_builder = gtk_builder

        self.gtk_dlg = self.get_widget('midi-select-dlg')
        self.connect_btn = self.get_widget('midi-connect-btn')
        self.connect_btn.connect('clicked', self.on_btn_connect_clicked)
        self.auto_connect_btn = self.get_widget('midi-auto-connect-btn')
        self.auto_connect_btn.connect('clicked', self.on_auto_connect_btn_clicked)
        cancel_btn = self.get_widget('midi-cancel-btn')
        cancel_btn.connect('clicked', self.on_cancel_btn_clicked)

        self.msg_spin_satck = self.get_widget('midi-message-spinner-stack')
        self.msg_lbl = self.get_widget('midi-select-message-lbl')
        self.midi_in_cbx = self.get_widget('midi-in-cbx')
        self.midi_out_cbx = self.get_widget('midi-out-cbx')
        self.midi_channel_spbtn = self.get_widget('midi-channel-spbtn')
        self.sysex_device_id_spbtn = self.get_widget('sysex-device-id-spbtn')

        self.msg_lbl.set_text('')

        self.midi_in_ports = self.js_interface.midi_in_ports.keys()
        self.midi_out_ports = self.js_interface.midi_out_ports.keys()
        self.populate_combo_box(self.midi_in_cbx, self.midi_in_ports)
        self.populate_combo_box(self.midi_out_cbx, self.midi_out_ports)

        self.port_in = None
        self.port_out = None

        self.is_connected = False
        self.is_valid = True

    def populate_combo_box(self, combo_box, midi_ports):
            midi_cbx_model = combo_box.get_model()
            for port in midi_ports:
                midi_cbx_model.append([port])
            cell = Gtk.CellRendererText()
            combo_box.pack_start(cell, True)
            combo_box.add_attribute(cell, 'text', 0)
            if midi_ports > 0:
                combo_box.set_active(0)


    def get_widget(self, widget_name):
        widget = self.gtk_builder.get_object(widget_name)
        if widget == None:
            self.is_valid = False
            print('Could not find widget %s'%(widget_name))
        return widget

    def set_defaults(self, midi_port_in, midi_port_out):
        # TODO: also set MIDI and sysex channels
        self.port_in = midi_port_in
        self.port_out = midi_port_out

        for index in range(0, len(self.midi_in_ports)):
            if self.port_in == self.midi_in_ports[index]:
                self.midi_in_cbx.set_active(index)
                break

        for index in range(0, len(self.midi_out_ports)):
            if self.port_out == self.midi_out_ports[index]:
                self.midi_out_cbx.set_active(index)
                break


    def present(self, widget=None):
        self.gtk_dlg.present()

    def hide(self):
        self.gtk_dlg.hide()


    def on_btn_connect_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.connect_disconnect, name='(dis)connect').start()

    def connect_disconnect(self):
        if not self.is_connected:
            port_in_cbx_index = self.midi_in_cbx.get_active()
            self.port_in  = self.midi_in_ports[port_in_cbx_index]
            port_out_cbx_index = self.midi_out_cbx.get_active()
            self.port_out = self.midi_out_ports[port_out_cbx_index]
            self.attempt_to_connect(self.port_in, self.port_out)
        else:
            self.js_interface.disconnect()
            self.set_disconnected()
        self.post_connection_actions()

    def on_auto_connect_btn_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.auto_connect, name='auto connect').start()

    def auto_connect(self):
        is_connected = False
        for port_in_index in range(0, len(self.midi_in_ports)):
            for port_out_index in range(0, len(self.midi_out_ports)):
                self.midi_in_cbx.set_active(port_in_index)
                self.midi_out_cbx.set_active(port_out_index)
                self.port_in = self.midi_in_ports[port_in_index]
                self.port_out = self.midi_out_ports[port_out_index]
                self.attempt_to_connect(self.port_in, self.port_out)
                if self.is_connected:
                    break
            if self.is_connected:
                break
        self.post_connection_actions()

    def pre_connection_actions(self):
        self.msg_spin_satck.set_visible_child_name('spinner')
        self.msg_lbl.set_text('')
        self.gtk_dlg.set_sensitive(False)

    def post_connection_actions(self):
        if self.is_connected:
            self.set_connected()
            self.on_connected(self.port_in, self.port_out)
        else:
            self.msg_lbl.set_text('Disconnect from J-Station')
        self.msg_spin_satck.set_visible_child_name('message')
        self.gtk_dlg.set_sensitive(True)


    def set_connected(self):
        self.is_connected = True
        self.connect_btn.set_label('Disconnect')
        self.connect_btn.set_sensitive(True)
        self.auto_connect_btn.set_sensitive(False)

    def set_disconnected(self):
        self.is_connected = False
        self.connect_btn.set_label('Connect')
        self.connect_btn.set_sensitive(True)
        self.auto_connect_btn.set_sensitive(True)

    def on_cancel_btn_clicked(self, widget):
        self.gtk_dlg.hide()
        if self.on_close:
            self.on_close()

    def attempt_to_connect(self, port_in, port_out):
        # TODO: read sysexchannel too
        print('Attempting to connect to %s and %s'%(port_in, port_out))
        self.js_interface.connect(port_in, port_out, 1)
        self.is_connected = self.js_interface.is_connected
