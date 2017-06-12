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

import sys
import os

from ConfigParser import SafeConfigParser


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from gstation_edit.midi_select_dlg import MidiSelectDlg

from sniffer.jstation_sniffer import JStationSniffer

sys.argv[0] = 'jstation-sniffer'

class JStationSnifferApp:
    def __init__( self ):
        GObject.threads_init()

        self.config = SafeConfigParser(allow_no_value=True)
        config_base_path = os.path.expanduser('~/.config/gstation-edit')
        if not os.path.isdir(config_base_path):
            os.makedirs(config_base_path)
        self.config_path = os.path.join(config_base_path, 'settings.cfg')
        self.config.read(self.config_path)


        gtk_builder_file = os.path.join('gstation_edit/resources',
                                        'gstation-edit-one-window.ui')

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_file(gtk_builder_file)

        self.js_sniffer = JStationSniffer(sys.argv[0])
        self.midi_dlg = MidiSelectDlg(self.gtk_builder, self,
                                      self.js_sniffer,
                                      self.on_connected, self.quit)
        self.midi_dlg.gtk_dlg.connect('destroy', self.quit)

        self.connect()

    def connect(self):
        midi_port_in = None
        midi_port_out = None
        if self.config.has_section('MIDI'):
            midi_port_in = self.config.get('MIDI', 'port_in')
            midi_port_out = self.config.get('MIDI', 'port_out')
            sysex_channel = self.config.getint('MIDI', 'sysex_channel')

        if midi_port_in and midi_port_out:
            self.js_sniffer.connect(midi_port_in, midi_port_out, sysex_channel)
            if self.js_sniffer.is_connected:
                self.midi_dlg.set_defaults(midi_port_in, midi_port_out)
                self.midi_dlg.set_connected()
                self.on_connected(midi_port_in, midi_port_out, sysex_channel)

        self.midi_dlg.present()

    def on_connected(self, midi_port_in, midi_port_out, sysex_channel):
        if self.js_sniffer.is_connected:
            if not self.config.has_section('MIDI'):
                self.config.add_section('MIDI')
            self.config.set('MIDI', 'port_in', midi_port_in)
            self.config.set('MIDI', 'port_out', midi_port_out)
            self.config.set('MIDI', 'sysex_channel', '%d'%(sysex_channel))

        self.js_sniffer.start_sniffer()
        self.midi_dlg.msg_lbl.set_text('Sniffing events...')

    def quit(self, window=None):
        print('Quitting jstation-sniffer')
        with open(self.config_path, 'wb') as configfile:
            self.config.write(configfile)

        self.js_sniffer.disconnect()
        Gtk.main_quit(self.midi_dlg)

def run():
    jstation_sniffer = JStationSnifferApp()
    Gtk.main()
