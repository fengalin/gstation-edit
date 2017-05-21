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

from .jstation_sysex_event import *
from .program import *

class ReceiveProgramUpdate(JStationSysExEvent):
    PROCEDURE_ID = 0x61
    VERSION = 2

    def __init__(self, channel=-1, seq_event=None, program=None):
        JStationSysExEvent.__init__(self, channel, seq_event)
        self.program = program

        if self.is_valid:
            prg_data_len = self.read_next_bytes(4)

            prg_buffer = self.data_buffer[self.data_index:]
            if len(prg_buffer) >= prg_data_len:
                has_changed = False
                if self.VERSION == 2:
                    has_changed = self.read_next_bytes(1)
                    prg_buffer = self.data_buffer[self.data_index:]

                self.program = Program(data_buffer=prg_buffer,
                                       has_changed=has_changed)
                self.is_valid = True
            else:
                self.is_valid = False
                print('Inconsistent prg len declared (%d) '\
                      'and available (%d)'%(prg_data_len, len(prg_data)))



    def build_data_buffer(self):
        JStationSysExEvent.build_data_buffer(self)
        if self.is_valid:
            program_changed_flag = 0
            if self.program.has_changed:
                program_changed_flag = 1
            data = list()
            data.append(program_changed_flag)
            data += self.program.data
            # TODO: check name length
            for index in range(0, len(self.program.name)):
                data.append(ord(self.program.name[index]))
            data.append(0) # 0 ending for name
            self.data_buffer += self.get_sysex_buffer(data)
        else:
            print('Could not build ReceiveProgramUpdateRequest')


    def __str__(self):
        return "%s, %s"%(JStationSysExEvent.__str__(self),
                         self.program.__str__())
