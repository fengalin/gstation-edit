"""
 gstation-edit ReceiveProgramUpdateResponse definition
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

from .prg_resp import *

class ReceiveProgramUpdateResponse(ProgramResponse):
    PROCEDURE_ID = 0x61
    COUNT_POS = 8
    CHANGED_FLAG_POS = 12
    PRG_DATA_LEN = 44

    PRG_DATA_POS_V1 = 12
    PRG_NAME_POS_V1 = 100
    PRG_DATA_POS_V2 = 14
    PRG_NAME_POS_V2 = 102

    PRG_DATA_POS = PRG_DATA_POS_V2
    PRG_NAME_POS = PRG_NAME_POS_V2

    def __init__(self, callback=None, seq_event=None):
        ProgramResponse.__init__(self, callback=callback, seq_event=seq_event)

        self.changed_flag = False
        if self.is_valid:
            if self.PRG_DATA_POS < len(self.data_buffer):
                if 2 == self.version:
                    # extra changed flag in version 2
                    self.changed_flag = self.get_value_from_split_bytes(
                        self.data_buffer[self.CHANGED_FLAG_POS: self.CHANGED_FLAG_POS+2]
                    )
                    self.PRG_DATA_POS = self.PRG_DATA_POS_V2
                    self.PRG_NAME_POS = self.PRG_NAME_POS_V2
                else:
                    self.PRG_DATA_POS = self.PRG_DATA_POS_V1
                    self.PRG_NAME_POS = self.PRG_NAME_POS_V1

                self.init_program(-1, -1)
            else:
                print('Data buffer is too short for message OneProgramResponse')
                self.is_valid = False

    def __str__(self):
        return "%s, changed %d, %s"%(ProgramResponse.__str__(self),
                                     self.changed_flag,
                                     self.prg.__str__())
