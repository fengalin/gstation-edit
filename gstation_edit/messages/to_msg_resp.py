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

from .jstation_sysex_resp import *

class ToMessageResponse(JStationSysExResponse):
    PROCEDURE_ID = 0x7f
    EXPECTED_DATA_LEN = 2
    REQ_PROCEDURE_POS = 8
    ERROR_CODE_POS = 10

    # TODO: there is no response length in this message => bypass it in base class

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback, seq_event=seq_event)
        self.req_procedure = -1
        self.error_code = -1

        if self.is_valid:
            # no length in this message
            self.req_procedure = self.get_value_from_split_bytes(
                self.data_buffer[self.REQ_PROCEDURE_POS : self.REQ_PROCEDURE_POS+2]
            )
            self.error_code = self.get_value_from_split_bytes(
                self.data_buffer[self.ERROR_CODE_POS : self.ERROR_CODE_POS+2]
            )
            self.is_valid = True

    def __str__(self):
        return "%s, request procedure: x%02x, error code: %d"\
                %(JStationSysExResponse.__str__(self),
                  self.req_procedure, self.error_code)

