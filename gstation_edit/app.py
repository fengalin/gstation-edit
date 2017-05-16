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

from main_window import *

try:
    from config import DATA_ROOT_DIR
except:
    DATA_ROOT_DIR = os.path.join('resources')

sys.argv[0] = 'gstation-edit'

class GStationEdit:
    def __init__( self ):
        GObject.threads_init()

        gtk_builder_file = os.path.join(DATA_ROOT_DIR, 'gstation-edit-one-window.ui')

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_file(gtk_builder_file)

        self.is_valid = False
        self.main_window = MainWindow(self.gtk_builder)

        signal_handlers = dict()
        signal_handlers['on_jstation-edit-window_destroy'] = self.quit
        signal_handlers.update(self.main_window.get_signal_handlers())

        self.gtk_builder.connect_signals(signal_handlers)

        self.main_window.connect()

    def quit(self, window):
        print('quitting gstation-edit')
        self.main_window.quit()
        Gtk.main_quit(window)

if __name__ == "__main__":
    gstation_edit = GStationEdit()
    Gtk.main()
