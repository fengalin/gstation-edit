"""
 gstation-edit OneProgramDump definition
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
from gstation_edit.messages.one_prg_resp import OneProgramResponse
from gstation_edit.messages.program import Program

class OneProgramDump(JStationSysExEvent):
    PROCEDURE_ID = 0x70
    VERSION = 1

    HEADER_LEN = 21

    def __init__(self, sysex_buffer=None, program=None, isolated=False):
        self.bank = -1
        self.number = -1
        self.program = None
        self.isolated = isolated
        if program:
            self.program = program.copy()
            if isolated:
                self.program.number = 0

            self.bank = self.program.bank
            self.number = self.program.number

        self.sysex_buffer = None
        self.rem_sysex_buffer = None
        if sysex_buffer:
            # buffer should consist in 2 messages
            # first part is a header of 21 bytes
            # second part is a OneProgramResponse
            if len(sysex_buffer) > self.HEADER_LEN:
                self.sysex_buffer = sysex_buffer[:self.HEADER_LEN]
                self.rem_sysex_buffer = sysex_buffer[self.HEADER_LEN:]

        JStationSysExEvent.__init__(self, JStationSysExEvent.ALL_CHANNELS,
                                    sysex_buffer=self.sysex_buffer)

    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self)
        if self.is_valid:
            self.bank = self.read_next_bytes(2)
            self.number = self.read_next_bytes(2)
            self.unknown_data = self.read_next_bytes(2)
            self.null_len = self.read_next_bytes(4)
            if self.is_valid:
                self.isolated = (self.number == 0)

                # expecting a OneProgramResponse in the rest of the buffer
                if len(self.rem_sysex_buffer) > \
                        JStationSysExEvent.PROCEDURE_ID_POS:
                    proc_id = self.rem_sysex_buffer[
                            JStationSysExEvent.PROCEDURE_ID_POS
                        ]
                    if proc_id == OneProgramResponse.PROCEDURE_ID:
                        one_prg_resp = OneProgramResponse(
                                JStationSysExEvent.ALL_CHANNELS,
                                sysex_buffer=self.rem_sysex_buffer
                            )
                        if one_prg_resp.is_valid:
                            self.program = one_prg_resp.program
                        else:
                            self.is_valid = False
                            print('Invalid nested event: %s'%(one_prg_resp))
                    else:
                        self.is_valid = False
                        print('Expected proc_id: x%02x, found: x%02x'\
                              %(OneProgramResponse.PROCEDURE_ID, proc_id))
                else:
                    self.is_valid = False
                    print('Too short buffer to read nested event proc_id')

    # Build to send
    def build_data_buffer(self):
        data_set = list()
        data_set.append(self.bank)
        data_set.append(self.number)
        data_set.append(1) # unknown data

        JStationSysExEvent.build_data_buffer(
            self,
            pre_len_data=data_set,
            post_len_data=[]
        )

    def build_sysex_buffer(self):
        JStationSysExEvent.build_sysex_buffer(self)
        if self.is_valid:
            one_prg_resp = OneProgramResponse(JStationSysExEvent.ALL_CHANNELS,
                                              program=self.program)
            if one_prg_resp.is_valid:
                self.sysex_buffer += one_prg_resp.sysex_buffer


    def __str__(self):
        suffix = ''
        if self.sysex_buffer:
            suffix = '\n%s'%(['x%02x'%(val & 0xff) for val in self.sysex_buffer])

        return '%s, %s%s'%(
                JStationSysExEvent.__str__(self),
                self.program.__str__(),
                suffix
            )
