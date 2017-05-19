"""
 gstation-edit SysExMidiEvent definition
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

from pyalsa import alsaseq

from .event import *

class SysExMidiEvent(MidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_SYSEX
    PROCEDURE_ID = 0x00
    PROCEDURE_ID_POS = 0x06

    SYSEX_DATA_KEY = 'ext'
    SYSEX_DATA_START = 0xf0
    SYSEX_DATA_END = 0xf7

    def __init__(self, seq_event=None):
        MidiEvent.__init__(self, self.EVENT_TYPE, seq_event)
        self.data_buffer = None

    def fill_seq_event(self):
        MidiEvent.fill_seq_event(self)
        self.build_data_buffer()
        if self.is_valid:
            sysex_data = list()
            sysex_data.append(self.SYSEX_DATA_START)
            sysex_data += self.data_buffer
            sysex_data.append(self.get_check_sum())
            sysex_data.append(self.SYSEX_DATA_END)

            event_data = dict()
            event_data[self.SYSEX_DATA_KEY] = sysex_data
            self.seq_event.set_data(event_data)

    def build_data_buffer(self):
        self.is_valid = False

    def get_check_sum(self):
        check_sum = 0
        for data in self.data_buffer:
            check_sum = check_sum ^ data
        return check_sum

    def get_value_from_split_bytes(self, split_bytes):
        value = 0
        split_bytes_range = len(split_bytes) / 2
        for index in range(0, split_bytes_range):
            byte_ = split_bytes[2*index + 1]
            if 0 != split_bytes[2*index]:
                byte_ += 0x80
            value = value + (byte_ << (8*index))
        return value

    def get_split_bytes_from_value(self, value, expected_bytes=2):
        split_bytes = list()
        remainder = value
        value_left_to_read = True
        while value_left_to_read or expected_bytes>len(split_bytes):
            current_byte = remainder & 0xff
            if current_byte & 0x80:
                split_bytes.append(1)
            else:
                split_bytes.append(0)
            split_bytes.append(current_byte & 0x7f)
            remainder = remainder >> 8
            if 0 == remainder:
                value_left_to_read = False

        return split_bytes
