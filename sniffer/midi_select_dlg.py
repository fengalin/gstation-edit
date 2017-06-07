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
    def __init__(self, parent, js_interface, gtk_builder):
        self.parent = parent
        self.js_interface = js_interface
        self.gtk_builder = gtk_builder

        self.gtk_dlg = self.get_widget('midi-select-dlg')
        connect_btn = self.get_widget('midi-connect-btn')
        connect_btn.connect('clicked', self.on_btn_connect_clicked)
        auto_connect_btn = self.get_widget('midi-auto-connect-btn')
        auto_connect_btn.connect('clicked', self.on_auto_connect_btn_clicked)
        cancel_btn = self.get_widget('midi-cancel-btn')
        cancel_btn.connect('clicked', self.on_cancel_btn_clicked)

        self.midi_select_msg_lbl = self.get_widget('midi-select_message-lbl')
        self.midi_in_cbx = self.get_widget('midi-in-cbx')
        self.midi_out_cbx = self.get_widget('midi-out-cbx')
        self.midi_channel_spbtn = self.get_widget('midi-channel-spbtn')
        self.sysex_device_id_spbtn = self.get_widget('sysex-device-id-spbtn')

        self.midi_select_msg_lbl.set_text('')

        self.midi_port_in_list = None
        self.midi_port_out_list = None

        self.midi_port_in_list = self.js_interface.midi_in_ports
        self.midi_port_out_list = self.js_interface.midi_out_ports
        self.populate_combo_box(self.midi_in_cbx, self.midi_port_in_list)
        self.populate_combo_box(self.midi_out_cbx, self.midi_port_out_list)

        self.is_valid = True

    def populate_combo_box(self, combo_box, midi_ports):
            midi_cbx_model = combo_box.get_model()
            for port in midi_ports:
                midi_cbx_model.append([port.port_name])
            cell = Gtk.CellRendererText()
            combo_box.pack_start(cell, True)
            combo_box.add_attribute(cell, 'text', 0)
            if midi_ports > 0:
                combo_box.set_active(0)


    def get_widget(self, widget_name):
        widget = self.gtk_builder.get_object(widget_name)
        if widget == None:
            self.is_valid = False
            print('Could not find widget %s'%(i_widget_name))
        return widget


    def present(self):
        self.gtk_dlg.present()


    def on_btn_connect_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.connect, name='connect').start()

    def connect(self):
        port_in_cbx_index = self.midi_in_cbx.get_active()
        port_in  = self.midi_port_in_list[port_in_cbx_index]
        port_out_cbx_index = self.midi_out_cbx.get_active()
        port_out = self.midi_port_out_list[port_out_cbx_index]
        if self.attempt_to_connect(port_in, port_out):
            self.js_interface.connect_sniffer(port_in, port_out)
            self.midi_select_msg_lbl.set_text('Connected to J-Station')
        else:
            self.midi_select_msg_lbl.set_text('Could not connect to J-Station')
        self.post_connection_actions()

    def on_auto_connect_btn_clicked(self, widget):
        self.pre_connection_actions()
        Thread(target=self.auto_connect, name='auto connect').start()

    def auto_connect(self):
        is_connected = False
        port_in = None
        port_out = None
        for port_in_index in range(0 , len(self.midi_port_in_list)):
            for port_out_index in range( 0, len(self.midi_port_out_list)):
                self.midi_in_cbx.set_active(port_in_index)
                self.midi_out_cbx.set_active(port_out_index)
                port_in = self.midi_port_in_list[port_in_index]
                port_out = self.midi_port_out_list[port_out_index]
                self.widget.set_active(port_in_index)
                if self.attempt_to_connect(port_in, port_out):
                    is_connected = True
                    break
            if is_connected:
                break

        if is_connected:
            self.js_interface.connect_sniffer(port_in, port_out)
            self.midi_select_msg_lbl.set_text('Connected to J-Station')
        else:
            self.midi_select_msg_lbl.set_text('Could not connect to J-Station')
        self.post_connection_actions()

    def pre_connection_actions(self):
        self.msg_spin_satck.set_visible_child_name('spinner')
        self.midi_select_msg_lbl.set_text('')
        #self.gtk_dlg.set_sensitive(False)

    def post_connection_actions(self):
        self.msg_spin_satck.set_visible_child_name('message')
        self.gtk_dlg.set_sensitive(True)

    def on_cancel_btn_clicked(self, widget):
        self.js_interface.disconnect()
        self.parent.quit(self)

    def attempt_to_connect(self, port_in, port_out):
        # TODO: read sysexchannel too
        print('Attempt to connect to %s and %s'%(port_in, port_out))
        self.js_interface.connect(port_in, port_out, 1)
        return self.js_interface.is_connected
