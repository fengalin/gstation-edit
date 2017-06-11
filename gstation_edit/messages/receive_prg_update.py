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

from gstation_edit.messages.jstation_sysex_event import JStationSysexEvent
from gstation_edit.messages.program import Program

class ReceiveProgramUpdate(JStationSysexEvent):
    PROCEDURE_ID = 0x61
    VERSION = 2

    def __init__(self, channel=-1, sysex_buffer=None, program=None):
        self.program = program

        JStationSysexEvent.__init__(self, channel, sysex_buffer=sysex_buffer)


    def parse_data_buffer(self):
        JStationSysexEvent.parse_data_buffer(self)
        data_len = self.read_next_bytes(4)

        if self.is_valid():
            has_changed = False
            if self.version == 2:
                has_changed = self.read_next_bytes(2)
                data_len -= 1

            self.program = Program(sysex_buffer=self.sysex_buffer,
                                   data_len=data_len,
                                   has_changed=has_changed)
            if not self.program.is_valid:
                self.has_error = True


    # Build to send
    def build_data_buffer(self):
        JStationSysexEvent.build_data_buffer(
            self,
            post_len_data=self.program.get_data_buffer(with_has_changed=True)
        )


    def __str__(self):
        return '%s, %s'%(JStationSysexEvent.__str__(self), self.program)
