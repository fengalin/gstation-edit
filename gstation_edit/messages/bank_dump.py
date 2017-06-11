"""
 gstation-edit BankDump definition
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
from gstation_edit.messages.prg_set_dump import ProgramSetDump
from gstation_edit.messages.program import Program

class BankDump(JStationSysExEvent):
    PROCEDURE_ID = 0x71
    VERSION = 1


    def __init__(self, sysex_buffer=None, program_set=program_set):
        self.value1 = -1
        self.value2 = -1
        self.bank = -1
        self.program_set = None
        if program_set:
            self.bank = self.program_set[0].bank

        JStationSysExEvent.__init__(self, JStationSysExEvent.ALL_CHANNELS,
                                    sysex_buffer=sysex_buffer)

        if sysex_buffer != None and self.is_valid():
            # first part is a header (already parsed)
            # second part is a ProgramSetDump
            # followed by a list of OneProgramDump
            start_bank_dump = StartBankDumpResponse(
                    JStationSysExEvent.ALL_CHANNELS,
                    sysex_buffer=rself.sysex_buffer
                )
            if start_bank_dump.is_valid():
                self.program_set = list()
                while self.sysex_buffer.has_more():
                    one_prg_dump = OneProgramDump(
                            JStationSysExEvent.ALL_CHANNELS,
                            sysex_buffer=self.sysex_buffer
                        )
                    if one_prg_dump.is_valid():
                        self.program_set.append(one_prg_resp.program)
                    else:
                        self.has_error = True

                if self.program_set:
                    self.bank = self.program_set[0].bank
            else:
                self.has_error = False


    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self)
        if self.is_valid:
            # TODO: determine the meaning of these values
            self.value1 = self.read_next_bytes(2) # possibly the bank
            self.value2 = self.read_next_bytes(2)
            self.null_len = self.read_next_bytes(4)


    # Build to send
    def build_data_buffer(self):
        data_set = list()
        data_set.append(self.value1)
        data_set.append(self.value2)

        JStationSysExEvent.build_data_buffer(
            self,
            pre_len_data=data_set,
            post_len_data=[]
        )


    def build_sysex_buffer(self):
        JStationSysExEvent.build_sysex_buffer(self)
        if self.is_valid():
            start_bank_dump = StartBankDumpResponse(
                    JStationSysExEvent.ALL_CHANNELS,
                    program_set=self.program_set
                )
            if start_bank_dump.is_valid():
                self.sysex_buffer.append(start_bank_dump.sysex_buffer)
                # TODO: add the list of OneProgramDump
            else:
                self.has_error = True


    def __str__(self):
        suffix = ''
        if self.sysex_buffer.is_valid():
            suffix = '%s'%(self.sysex_buffer)

        # TODO: add program set

        return '%s, value1: %d, value2: %d, %s'%(
                JStationSysExEvent.__str__(self),
                self.value1, self.value2, suffix
            )
