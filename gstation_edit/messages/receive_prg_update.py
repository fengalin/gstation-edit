"""
 gstation-edit ReceiveProgramUpdateRequest definition
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

class ReceiveProgramUpdate(JStationSysExEvent):
    PROCEDURE_ID = 0x61
    VERSION = 2

    def __init__(self, channel=-1, seq_event=None, sysex_buffer=None,
                 program=None):
        self.program = program

        JStationSysExEvent.__init__(self, channel, seq_event=seq_event,
                                    sysex_buffer=sysex_buffer)

    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self, read_len=True)
        if self.is_valid:
            has_changed = False
            if self.version == 2:
                has_changed = self.read_next_bytes(2)

            prg_buffer = self.data_buffer[self.data_index:]
            self.program = Program(data_buffer=prg_buffer,
                                   has_changed=has_changed)


    # Build to send
    def build_data_buffer(self):
        JStationSysExEvent.build_data_buffer(
            self,
            post_len_data=self.program.get_data_buffer(with_has_changed=True)
        )


    def __str__(self):
        return '%s, %s'%(JStationSysExEvent.__str__(self),
                         self.program.__str__())
