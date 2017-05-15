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

from jstation_sysex_req import *

class ReceiveProgramUpdateRequest(JStationSysExRequest):
    def __init__(self, program, channel_id=0):
        JStationSysExRequest.__init__(self, channel_id=channel_id,
                                      procedure_id=0x61, version=2)
        self.program = program

    def build_data_buffer(self):
        JStationSysExRequest.build_data_buffer(self)
        if self.is_valid:
            program_changed_flag = 0
            if self.program.has_changed:
                program_changed_flag = 1
            data = list()
            data.append(program_changed_flag)
            data += self.program.data
            for index in range(0, len(self.program.name)):
                data.append(ord(self.program.name[index]))
            data.append(0) # 0 ending for name
            self.data_buffer = self.data_buffer + self.get_sysex_buffer(data)
        else:
            print('Could not build ReceiveProgramUpdateRequest')

    def __str__(self):
        return "%s. Version: %d"%(self.__class__.__name__, self.m_version)

