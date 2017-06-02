"""
 gstation-edit WhoAmIRequest definition
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

from .jstation_sysex_event import JStationSysExEvent

class WhoAmIRequest(JStationSysExEvent):
    PROCEDURE_ID = 0x40
    VERSION = 1

    RESP_ON_CHANNEL = 0
    RESP_ON_7f = 1

    def __init__(self, channel=JStationSysExEvent.ALL_CHANNELS, seq_event=None):
        JStationSysExEvent.__init__(self, channel, seq_event)
        self.response_on = self.RESP_ON_7f

        if self.is_valid:
            if len(self.data_buffer) >= 2:
                self.response_on = self.read_next_bytes(2)
                self.is_valid = True
            else:
                print('Data buffer is too short to get response_on_7f')
                self.is_valid = False


    # Build to send
    def build_data_buffer(self):
        if self.RESP_ON_CHANNEL == self.response_on or \
                self.RESP_ON_7f == self.response_on:
            JStationSysExEvent.build_data_buffer(
                self, data_after_len=[self.response_on]
            )
        else:
            self.data_buffer = list()
            self.is_valid = False
            print('Response on not defined for ReqWhoAmI SysEx')


    # Common
    def __str__(self):
        return "%s, response on: %d"%(JStationSysExEvent.__str__(self),
                                     self.response_on)
