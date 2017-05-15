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

from midi.port import *

class MidiSelectDlg:
    def __init__(self, rack, js_interface, gtk_builder):
        self.rack = rack
        self.js_interface = js_interface
        self.gtk_builder = gtk_builder

        self.midi_select_dlg = self.get_widget('midi-select-dlg')
        self.midi_select_msg_lbl = self.get_widget('midi-select_message-lbl')
        self.midi_in_cbx = self.get_widget('midi-in-cbx')
        self.midi_out_cbx = self.get_widget('midi-out-cbx')
        self.midi_channel_spbtn = self.get_widget('midi-channel-spbtn')
        self.sysex_device_id_spbtn = self.get_widget('sysex-device-id-spbtn')

        self.midi_select_msg_lbl.set_text( '' )

        self.midi_port_in_list = None
        self.midi_port_out_list = None

        # TODO: update validity
        self.is_valid = True

        if self.is_valid:
            self.midi_port_in_list = self.js_interface.midi_in_ports
            self.midi_port_out_list = self.js_interface.midi_out_ports
            self.populate_combo_box(self.midi_in_cbx, self.midi_port_in_list)
            self.populate_combo_box(self.midi_out_cbx, self.midi_port_out_list)


    def populate_combo_box(self, combo_box, midi_ports):
            midi_cbx_model = combo_box.get_model()
            for port in midi_ports:
                midi_cbx_model.append([port.port_name])
            cell = Gtk.CellRendererText()
            combo_box.pack_start(cell, True)
            combo_box.add_attribute(cell, 'text', 0)
            if 0 < midi_ports:
                combo_box.set_active(0)


    def get_widget(self, widget_name):
        widget = self.gtk_builder.get_object(widget_name)
        if None == widget:
            self.is_valid = False
            print('Could not find widget %s'%(i_widget_name))
        return widget


    def get_signal_handlers(self):
        signal_handlers = dict()
        signal_handlers['on_midi-select-dlg_close'] = self.on_cancel_btn_clicked
        signal_handlers['on_midi-connect-btn_clicked'] = self.on_btn_connect_clicked
        signal_handlers['on_midi-auto-connect-btn_clicked'] = self.on_auto_connect_btn_clicked
        signal_handlers['on_midi-cancel-btn_clicked'] = self.on_cancel_btn_clicked
        return signal_handlers


    def present(self):
        self.midi_select_dlg.present()


    def on_btn_connect_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.connect, name='connect').start()

    def connect(self):
        port_in_cbx_index = self.midi_in_cbx.get_active()
        port_in  = self.midi_port_in_list[port_in_cbx_index]
        port_out_cbx_index = self.midi_out_cbx.get_active()
        port_out = self.midi_port_out_list[port_out_cbx_index]
        if self.attempt_to_connect(port_in, port_out):
            self.midi_select_dlg.hide()
            self.rack.request_bank_dump()
        else:
            self.midi_select_msg_lbl.set_text('Could not connect to J-Station')
        self.post_connection_actions()

    def on_auto_connect_btn_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.auto_connect, name='auto connect').start()

    def auto_connect(self):
        is_connected = False
        for port_in_index in range(0 , len(self.midi_port_in_list)):
            for port_out_index in range( 0, len(self.midi_port_out_list)):
                port_in = self.midi_port_in_list[port_in_index]
                port_out = self.midi_port_out_list[port_out_index]
                if self.attempt_to_connect(port_in, port_out):
                    is_connected = True
                    break
            if is_connected:
                break

        if is_connected:
            self.midi_select_dlg.hide()
            self.rack.request_bank_dump()
        else:
            self.midi_select_msg_lbl.set_text('Could not connect to J-Station')
        self.post_connection_actions()

    def pre_connection_actions(self):
        # TDOO: fix cursor
        #self.midi_select_dlg.set_cursor(Gtk.gdk.Cursor(Gtk.gdk.WATCH))
        self.midi_select_msg_lbl.set_text('')
        self.midi_select_dlg.set_sensitive(False)

    def post_connection_actions(self):
        # TDOO: fix cursor
        #self.midi_select_dlg.set_cursor(None)
        self.midi_select_dlg.set_sensitive(True)

    def on_cancel_btn_clicked(self, widget):
        self.midi_select_dlg.hide()

    def attempt_to_connect(self, port_in, port_out):
        # TODO: read sysexchannel too
        print('Attempt to connect to %s and %s'%(str(port_in), str(port_out)))
        self.js_interface.connect(port_in, port_out, 1)
        return self.js_interface.is_connected
