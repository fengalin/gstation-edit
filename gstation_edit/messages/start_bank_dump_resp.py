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

from .jstation_sysex_resp import *

class StartBankDumpResponse(JStationSysExResponse):
    PROCEDURE_ID = 0x25
    EXPECTED_DATA_LEN = 2
    TOTAL_LEN_POS = 12
    TOTAL_LEN_END = 16

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback=callback, seq_event=seq_event)
        self.total_length = -1

        if self.is_valid:
            data_length = self.get_count()
            if self.EXPECTED_DATA_LEN == data_length:
                self.total_length = self.get_value_from_split_bytes(
                    self.data_buffer[self.TOTAL_LEN_POS : self.TOTAL_LEN_END]
                )
                self.is_valid = True
            else:
                print('Incorrect data length %d within WhoAmIResponse'%(data_length))
                self.is_valid = False

    def __str__(self):
        return "%s. Version: %d, total length: %d"%(self.__class__.__name__,
                                                    self.version,
                                                    self.total_length)

