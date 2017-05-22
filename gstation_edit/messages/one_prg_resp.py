"""
 gstation-edit OneProgramResponse definition
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

from .jstation_sysex_event import *
from .program import *

class OneProgramResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x02
    VERSION = 1

    def __init__(self, channel=-1, program=None, seq_event=None):
        JStationSysExEvent.__init__(self, channel, seq_event)

        self.program = program

        if self.is_valid:
            bank = self.read_next_bytes(2)
            number = self.read_next_bytes(2)
            prg_data_len = self.read_next_bytes(4)

            prg_data = self.data_buffer[self.data_index:]
            self.program = Program(bank, number, data_buffer=prg_data)


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    def __str__(self):
        return "%s, %s"%(JStationSysExEvent.__str__(self), self.program)

