"""
 gstation-edit PRGIndicesResponse definition
"""
# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009 <fengalin@free.fr>
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

class PRGIndicesResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x14
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None, sysex_buffer=None):
        self.prg_indices = list()

        JStationSysExEvent.__init__(self, channel, seq_event=seq_event,
                                    sysex_buffer=sysex_buffer)

    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self, read_len=True)
        if self.is_valid:
            for index in range(0, self.data_length):
                self.prg_indices.append(self.read_next_bytes(2))


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    def __str__(self):
        return "%s, prg indices: %s"%(JStationSysExEvent.__str__(self),
                                      str(self.prg_indices))

