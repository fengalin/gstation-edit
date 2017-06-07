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

        gtk_builder_file = os.path.join('gstation_edit/resources',
                                        'gstation-edit-one-window.ui')

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_file(gtk_builder_file)

        self.js_sniffer = JStationSniffer(sys.argv[0])
        self.main_window = MidiSelectDlg(self.gtk_builder, self,
                                         self.js_sniffer,
                                         self.start_sniffing, self.quit)

        self.main_window.gtk_dlg.connect('destroy', self.quit)

        self.main_window.present()

    def start_sniffing(self, midi_port_in, midi_port_out):
        self.js_sniffer.start_sniffer(midi_port_in, midi_port_out)
        self.main_window.msg_lbl.set_text('Sniffing events...')

    def quit(self, window=None):
        print('Quitting jstation-sniffer')
        self.js_sniffer.disconnect()
        Gtk.main_quit(self.main_window)

def run():
    jstation_sniffer = JStationSnifferApp()
    Gtk.main()
