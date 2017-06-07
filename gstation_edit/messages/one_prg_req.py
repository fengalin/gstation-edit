"""
 gstation-edit OneProgramRequest definition
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
from gstation_edit.messages.program import Program

class OneProgramRequest(JStationSysExEvent):
    PROCEDURE_ID = 0x01
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None, sysex_buffer=None,
                 bank_nb=-1, prg_nb=-1):
        self.bank_nb = bank_nb
        self.prg_nb = prg_nb

        JStationSysExEvent.__init__(self, channel, seq_event=seq_event,
                                    sysex_buffer=sysex_buffer)

    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self)
        self.bank_nb = self.read_next_bytes(2)
        self.prg_nb = self.read_next_bytes(2)


    # Build to send
    def build_data_buffer(self):
        JStationSysExEvent.build_data_buffer(
            self,
            pre_len_data=[self.bank_nb, self.prg_nb]
        )


    def __str__( self ):
        return '%s, %s bank, prg nb: %d'\
                %(JStationSysExEvent.__str__(self),
                  Program.get_bank_name(self.bank_nb), self.prg_nb)

