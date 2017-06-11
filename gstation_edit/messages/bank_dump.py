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

from gstation_edit.messages.jstation_sysex_event import JStationSysexEvent
from gstation_edit.messages.start_bank_dump_resp import StartBankDumpResponse
from gstation_edit.messages.end_bank_dump_resp import EndBankDumpResponse
from gstation_edit.messages.one_prg_dump import OneProgramDump
from gstation_edit.messages.program import Program

class BankDump(JStationSysexEvent):
    PROCEDURE_ID = 0x71
    VERSION = 1

    OneProgramDump.register()
    EndBankDumpResponse.register()


    def __init__(self, sysex_buffer=None, program_set=None):

        self.value1 = 1 # TODO: find out what this is: bank nb?
        self.value2 = 1 # TODO: find out what this is
        self.bank = -1
        self.program_set = None
        if program_set:
            self.bank = self.program_set[0].bank

        JStationSysexEvent.__init__(self, JStationSysexEvent.ALL_CHANNELS,
                                    sysex_buffer=sysex_buffer)

        if sysex_buffer != None and self.is_valid():
            # first part is a header (already parsed)
            # second part is a ProgramSetDump
            # followed by a list of OneProgramDump
            # and completed by a EndBankDumpResponse
            start_bank_dump = StartBankDumpResponse(
                    JStationSysexEvent.ALL_CHANNELS,
                    sysex_buffer=self.sysex_buffer
                )
            if start_bank_dump.is_valid():
                print('start_bank_dump %s'%(start_bank_dump))
                actual_len = 0
                self.program_set = list()
                last_event = None
                while self.sysex_buffer.has_more() and \
                                   not type(last_event) is EndBankDumpResponse:
                    last_index = self.sysex_buffer.data_index
                    last_event = JStationSysexEvent.build_from_sysex_buffer(
                            self.sysex_buffer)
                    if type(last_event) is OneProgramDump:
                        if last_event.is_valid():
                            actual_len += self.sysex_buffer.data_index - last_index
                            self.program_set.append(last_event.program)
                        else:
                            self.has_error = True

                if self.program_set:
                    self.bank = self.program_set[0].bank
                    print('actual_len: %d'%(actual_len))
            else:
                self.has_error = False


    def parse_data_buffer(self):
        JStationSysexEvent.parse_data_buffer(self)
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

        JStationSysexEvent.build_data_buffer(
            self,
            pre_len_data=data_set,
            post_len_data=[]
        )


    def build_sysex_buffer(self):
        JStationSysexEvent.build_sysex_buffer(self)
        if self.is_valid():
            start_bank_dump = StartBankDumpResponse(
                    JStationSysexEvent.ALL_CHANNELS,
                    program_set=self.program_set
                )
            if start_bank_dump.is_valid():
                self.sysex_buffer.append(start_bank_dump.sysex_buffer)

                for program in self.program_set:
                    prg_dump = OneProgramDump(program=program)
                    if prg_dump.is_valid():
                        self.sysex_buffer.append(prg_dump.sysex_buffer)
                    else:
                        self.has_error = True
                        break

                if self.is_valid():
                    end_bank_dump = EndBankDumpResponse(
                        JStationSysexEvent.ALL_CHANNELS)
                    if end_bank_dump.is_valid():
                        self.sysex_buffer.append(end_bank_dump.sysex_buffer)
                    else:
                        self.has_error = True
            else:
                self.has_error = True


    def __str__(self):
        programs = ''
        if self.program_set:
            programs = ', %d programs'%(len(self.program_set))

        return '%s, value1: %d, value2: %d%s'%(
                JStationSysexEvent.__str__(self),
                self.value1, self.value2, programs,
            )
