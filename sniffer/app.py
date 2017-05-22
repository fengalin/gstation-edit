#!/usr/bin/python
#
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

from .jstation_sniffer import *
from .midi_select_dlg import *

sys.argv[0] = 'jstation-sniffer'

class JStationSnifferApp:
    def __init__( self ):
        GObject.threads_init()

        gtk_builder_file = os.path.join('sniffer/resources', 'jstation_sniffer.ui')

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_file(gtk_builder_file)

        self.main_window = MidiSelectDlg(self,
                                         JStationSniffer(sys.argv[0]),
                                         self.gtk_builder)

        signal_handlers = dict()
        signal_handlers['on_jstation-sniffer-window_destroy'] = self.quit
        signal_handlers.update(self.main_window.get_signal_handlers())

        self.gtk_builder.connect_signals(signal_handlers)

        self.main_window.present()

    def quit(self, window):
        print('quitting jstation-sniffer')
        Gtk.main_quit(window)

def run():
    jstation_sniffer = JStationSnifferApp()
    Gtk.main()
