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

from jstation_sysex_resp import *

class PRGIndicesResponse(JStationSysExResponse):
    PROCEDURE_ID = 0x14
    PRG_INDICES_POS = 12

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback=callback, seq_event=seq_event)
        self.prg_indices = list()
        if self.is_valid:
            data_length = self.get_count()
            index = 0
            while index < data_length:
                pos = self.PRG_INDICES_POS + 2*index
                self.prg_indices.append(self.get_value_from_split_bytes(
                                            self.data_buffer[pos : pos+2]
                                        )
                )
                index += 1
            self.is_valid = True

    def __str__(self):
        return "%s. Version: %d, prg indexes: %s"%(self.__class__.__name__,
                                                   self.version,
                                                   str(self.m_prg_indices))

