"""
 gstation-edit JStationInterface test
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

from gstation_edit.jstation_interface import *

def test():
    print('\n==== JStationInterface test')
    jstation_interface = JStationInterface('JStationInterface test', None)
    jstation_interface.get_clients()
    for midi_port in jstation_interface.midi_in_ports:
        print(midi_port)
    for midi_port in jstation_interface.midi_out_ports:
        print(midi_port)
