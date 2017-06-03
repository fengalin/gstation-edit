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

from gstation_edit.messages.jstation_sysex_event import JStationSysExEvent
from gstation_edit.messages.program import Program

class OneProgramResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x02
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None, program=None):
        JStationSysExEvent.__init__(self, channel, seq_event)

        self.program = program

        if self.is_valid:
            bank_nb = self.read_next_bytes(2)
            prg_nb = self.read_next_bytes(2)
            prg_data_len = self.read_next_bytes(4)

            prg_data = self.data_buffer[self.data_index:]
            self.program = Program(bank_nb, prg_nb, data_buffer=prg_data)

    # Build to send
    def build_data_buffer(self):
        JStationSysExEvent.build_data_buffer(
            self,
            data_before_len=[self.program.bank, self.program.number],
            data_after_len=self.program.get_data_buffer()
        )


    def __str__(self):
        return "%s, %s"%(JStationSysExEvent.__str__(self), self.program)

