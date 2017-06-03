"""
 gstation-edit WhoAmIResponse definition
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

class WhoAmIResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x41
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None,
                 receive_channel=-1, transmit_channel=-1, sysex_channel=-1):
        JStationSysExEvent.__init__(self, channel, seq_event)
        self.receive_channel = receive_channel
        self.transmit_channel = transmit_channel
        self.sysex_channel = sysex_channel

        if self.is_valid:
            data_length = self.read_next_bytes(4)
            if len(self.data_buffer)-4 >= data_length:
                self.receive_channel = self.read_next_bytes(2)
                self.transmit_channel = self.read_next_bytes(2)
                self.sysex_channel = self.read_next_bytes(2)
                self.is_valid = True
            else:
                print('Incorrect data buffer with len %d. Expecting %d'\
                      %(len(self.data_buffer)-4, data_length))
                self.m_is_valid = False


    # Build to send
    def build_data_buffer(self):
        print('Not implemented yet')


    # Common
    def __str__(self):
        return "%s, receive ch: %d, transmit ch: %d, "\
                "sysex ch: %d"%(JStationSysExEvent.__str__(self),
                                self.receive_channel, self.transmit_channel,
                                self.sysex_channel)

