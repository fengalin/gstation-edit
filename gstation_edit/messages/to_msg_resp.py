"""
 gstation-edit ToMessageResponse definition
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

class ToMessageResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x7f
    VERSION = 1

    ERRORS = {
         0: 'OK',
         1: 'Unknown Procedure Id',
         2: 'Invalid Procedure Version',
         3: 'Sysex Message Checksum Error',
         4: 'Sysex Request Wrong Size',
         5: 'MIDI Overrun Error',
         6: 'Invalid Program Number',
         7: 'Invalid User Program Number',
         8: 'Invalid Bank Number',
         9: 'Wrong Data Count',
        10: 'Unknown OS Command',
        11: 'Wrong Mode for OS Command'
    }

    def __init__(self, channel=-1, seq_event=None,
                 req_procedure=-1, error_code=-1):
        JStationSysExEvent.__init__(self, channel, seq_event)
        self.req_procedure = req_procedure
        self.error_code = error_code
        self.error_msg = ''

        if self.is_valid:
            # no length in this message
            self.req_procedure = self.read_next_bytes(2)
            self.error_code = self.read_next_bytes(2)
            self.error_msg = self.ERRORS.get(self.error_code)
            if self.error_msg == None:
                 self.error_msg = '*Unknown code*'
            self.is_valid = True


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    def __str__(self):
        return '%s, request procedure: x%02x, message: %s (%d)'\
                %(JStationSysExEvent.__str__(self),
                  self.req_procedure, self.error_msg, self.error_code)

