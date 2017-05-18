"""
 gstation-edit ProgramResponse definition
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

from ..program import *
from .jstation_sysex_resp import *

class ProgramResponse(JStationSysExResponse):
    # constants to be defined in heirs:
    # COUNT_POS
    # PRG_DATA_POS
    # PRG_DATA_LEN
    # PRG_NAME_POS

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback=callback, seq_event=seq_event)
        self.prg = None

    def init_program(self, bank=0, number=0):
        data_length = self.get_count(self.COUNT_POS)
        index = 0
        data = list()
        while index < self.PRG_DATA_LEN:
            pos = self.PRG_DATA_POS + 2*index
            data.append(self.get_value_from_split_bytes(self.data_buffer[pos : pos+2]))
            index += 1
        index = 0
        name = ''
        while index < data_length:
            pos = self.PRG_NAME_POS + 2*index
            value = self.get_value_from_split_bytes(self.data_buffer[pos : pos+2])
            if 0 != value:
                name = name + chr(value)
            else:
                break
            index += 1
        self.prg = Program(bank, number, data, name)
        self.is_valid = True

