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
