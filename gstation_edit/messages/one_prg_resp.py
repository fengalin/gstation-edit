"""
 gstation-edit OneProgramResponse definition
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

from prg_resp import *

class OneProgramResponse(ProgramResponse):
    PROCEDURE_ID = 0x02
    PRG_BANK_POS = 8
    PRG_NUMBER_POS = 10
    COUNT_POS = 12
    PRG_DATA_POS = 16
    PRG_DATA_LEN = 44
    PRG_NAME_POS = 104

    def __init__(self, callback=None, seq_event=None):
        ProgramResponse.__init__(self, callback=callback, seq_event=seq_event)
        if self.is_valid:
            if self.PRG_DATA_POS < len(self.data_buffer):
                bank = self.get_value_from_split_bytes(
                   self.data_buffer[self.PRG_BANK_POS : self.PRG_BANK_POS+2]
                )
                number = self.get_value_from_split_bytes(
                    self.data_buffer[self.PRG_NUMBER_POS : self.PRG_NUMBER_POS+2]
                )

                self.init_program(bank, number)
            else:
                print('Data buffer is too short for message OneProgramResponse')
                self.is_valid = False


    def __str__(self):
        return "%s. Version: %d, %s"%(self.__class__.__name__,
                                      self.version,
                                      self.prg.__str__())

