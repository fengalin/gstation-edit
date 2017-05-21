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

from .jstation_sysex_event import *

class PRGIndicesResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x14
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None):
        JStationSysExEvent.__init__(self, channel, seq_event)

        self.prg_indices = list()
        if self.is_valid:
            data_length = self.read_next_bytes(4)

            if len(self.data_buffer)-4 >= data_length:
                while self.data_index < data_length:
                    self.prg_indices.append(self.read_next_bytes(2))
                self.is_valid = True
            else:
                self.is_valid = False
                data_buffer = None
                print('Inconsistent data len declared (%d) '\
                      'and left for data (%d)'%(data_len,
                                                len(self.data_buffer)-4))


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    def __str__(self):
        return "%s, prg indices: %s"%(JStationSysExEvent.__str__(self),
                                      str(self.prg_indices))

