# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009-2021 <fengalin@free.fr>
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

import configparser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

import pkg_resources
gstation_edit_ui = pkg_resources.resource_string(
    __name__,
    'resources/gstation-edit-one-window.ui',
).decode('utf-8')

from gstation_edit.main_window import MainWindow

sys.argv[0] = 'gstation-edit'

class GStationEdit:
    def __init__( self ):
        GObject.threads_init()

        self.config = configparser.ConfigParser(allow_no_value=True)
        config_base_path = os.path.expanduser('~/.config/gstation-edit')
        if not os.path.isdir(config_base_path):
            os.makedirs(config_base_path)
        self.config_path = os.path.join(config_base_path, 'settings.cfg')
        self.config.read(self.config_path)

        self.gtk_builder = Gtk.Builder()
        self.gtk_builder.add_from_string(gstation_edit_ui)

        self.main_window = MainWindow(sys.argv[0], self.config, self.gtk_builder)
        self.main_window.gtk_window.connect('destroy', self.quit)

    def quit(self, window):
        print('quitting gstation-edit')
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

        self.main_window.quit()
        Gtk.main_quit(window)

def run():
    gstation_edit_app = GStationEdit()
    Gtk.main()
