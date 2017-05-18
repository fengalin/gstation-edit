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

from .jstation_sysex_resp import *

class WhoAmIResponse(JStationSysExResponse):
    PROCEDURE_ID = 0x41
    EXPECTED_DATA_LEN = 3
    RECEIVE_CHANNEL_POS = 12
    RECEIVE_CHANNEL_POS_END = 14
    TRANSMIT_CHANNEL_POS = 14
    TRANSMIT_CHANNEL_POS_END = 16
    SYSEX_CHANNEL_POS = 16
    SYSEX_CHANNEL_POS_END = 18

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback, seq_event=seq_event)
        self.receive_channel = -1
        self.transmit_channel = -1
        self.sysex_channel = -1

        if self.is_valid:
            data_length = self.get_count()
            if self.EXPECTED_DATA_LEN == data_length:
                self.receive_channel = self.get_value_from_split_bytes(
                    self.data_buffer[self.RECEIVE_CHANNEL_POS : self.RECEIVE_CHANNEL_POS_END]
                )
                self.transmit_channel = self.get_value_from_split_bytes(
                   self.data_buffer[self.TRANSMIT_CHANNEL_POS : self.TRANSMIT_CHANNEL_POS_END]
                )
                self.sysex_channel = self.get_value_from_split_bytes(
                    self.data_buffer[ self.SYSEX_CHANNEL_POS : self.SYSEX_CHANNEL_POS_END]
                )
                self.is_valid = True
            else:
                print('Incorrect data length %d within WhoAmIResponse'%(data_length))
                self.is_valid = False

    def __str__(self):
        return "%s. Version: %d, receive ch: %d, transmit ch: %d, "\
                "sysex ch: %d"%(self.__class__.__name__,
                                self.version,
                                self.receive_channel,
                                self.transmit_channel,
                                self.sysex_channel)

