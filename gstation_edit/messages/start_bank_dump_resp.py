"""
 gstation-edit StartBankDumpResponse definition
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

class StartBankDumpResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x25
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None, total_length=-1):
        self.total_length = total_length

        JStationSysExEvent.__init__(self, channel, seq_event=seq_event)


    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self)
        data_len = self.read_next_bytes(4)

        if self.is_valid():
            self.total_length = self.read_next_bytes(2*data_len)


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    def __str__(self):
        return '%s, total length: %d'%(JStationSysExEvent.__str__(self),
                                       self.total_length)
