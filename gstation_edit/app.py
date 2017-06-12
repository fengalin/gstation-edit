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

from gstation_edit.main_window import MainWindow

try:
    from config import DATA_ROOT_DIR
except:
    DATA_ROOT_DIR = os.path.join('gstation_edit', 'resources')

sys.argv[0] = 'gstation-edit'

class GStationEdit:
    def __init__( self ):
        GObject.threads_init()

        self.config = SafeConfigParser(allow_no_value=True)
        config_base_path = os.path.expanduser('~/.config/gstation-edit')
        if not os.path.isdir(config_base_path):
            os.makedirs(config_base_path)
        self.config_path = os.path.join(config_base_path, 'settings.cfg')
        self.config.read(self.config_path)

        gtk_builder_file = os.path.join(DATA_ROOT_DIR,
                                        'gstation-edit-one-window.ui')

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_file(gtk_builder_file)

        self.is_valid = False
        self.main_window = MainWindow(sys.argv[0], self.config, self.gtk_builder)
        self.main_window.gtk_window.connect('destroy', self.quit)

        self.main_window.connect()

    def quit(self, window):
        print('quitting gstation-edit')
        with open(self.config_path, 'wb') as configfile:
            self.config.write(configfile)

        self.main_window.quit()
        Gtk.main_quit(window)

def run():
    gstation_edit_app = GStationEdit()
    Gtk.main()
