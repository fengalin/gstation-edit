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

from gstation_edit.midi.split_bytes import SplitBytesHelpher

from gstation_edit.messages.jstation_sysex_event import JStationSysexEvent

class StartBankDumpResponse(JStationSysexEvent):
    PROCEDURE_ID = 0x25
    VERSION = 1

    def __init__(self, channel=-1, sysex_buffer=None, total_len=-1):
        self.total_len = total_len

        JStationSysexEvent.__init__(self, channel, sysex_buffer=sysex_buffer)


    def parse_data_buffer(self):
        JStationSysexEvent.parse_data_buffer(self)
        data_len = self.read_next_bytes(4)
        if data_len > 2:
            # For some reasons, data len in a bank export from J-Edit
            # is 4 when the actual size to read is 2 just like
            # for the regular StartBankDumpResponse sent by the J-Station
            print('Fixing data len %d for StartBankDumpResponse'%(data_len))
            data_len = 2

        if self.is_valid():
            self.total_len = self.read_next_bytes(2*data_len)


    # Build to send
    def build_data_buffer(self):
        total_len_2_bytes = [self.total_len%0x100, self.total_len//0x100]
        JStationSysexEvent.build_data_buffer(
            self,
            post_len_data=total_len_2_bytes
        )


    def __str__(self):
        return '%s, total total_len: %d'%(JStationSysexEvent.__str__(self),
                                       self.total_len)
