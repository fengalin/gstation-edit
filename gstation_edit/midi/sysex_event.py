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

from gstation_edit.midi.event import MidiEvent

class SysExMidiEvent(MidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_SYSEX
    PROCEDURE_ID = 0x00
    PROCEDURE_ID_POS = 0x06

    SYSEX_DATA_KEY = 'ext'
    SYSEX_DATA_START = 0xf0
    SYSEX_DATA_END = 0xf7

    def __init__(self, seq_event=None, sysex_buffer=None):
        MidiEvent.__init__(self, self.EVENT_TYPE, seq_event)

        self.sysex_buffer = sysex_buffer
        self.data_buffer = None
        self.data_index = -1

        if seq_event:
            sysex_content = \
                seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
            if sysex_content:
                self.sysex_buffer = sysex_content
            else:
                self.sysex_buffer = None
                print('Not a sysex event: %d'\
                      %(seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)))

        if self.sysex_buffer:
            self.parse_sysex_buffer()

    def parse_sysex_buffer(self):
        # SysEx data expected structure: 0xf0 ... data ... checksum 0xf7
        len_sysex = len(self.sysex_buffer)
        if len_sysex > 3:
            if self.sysex_buffer[0] == self.SYSEX_DATA_START \
                    and self.sysex_buffer[len_sysex-1] == self.SYSEX_DATA_END:

                self.data_buffer = self.sysex_buffer[1: len_sysex-2]
                self.data_index = 0

                check_sum = self.sysex_buffer[len_sysex-2]
                self.is_valid = (check_sum == self.get_check_sum())
                if self.is_valid:
                    self.parse_data_buffer()
                else:
                    print('Incorrect checksum for sysex buffer: %s'
                        %(['x%02x'%(val & 0xff) for val in self.sysex_buffer])
                    )

    def parse_data_buffer(self):
        # To be implemented in heirs
        self.is_valid = False


    # Build to send

    def build_data_buffer(self):
        # To be implemented in heirs
        self.is_valid = False

    def build_sysex_buffer(self):
        self.build_data_buffer()
        if self.is_valid:
            self.sysex_buffer = list()
            self.sysex_buffer.append(self.SYSEX_DATA_START)
            self.sysex_buffer += self.data_buffer
            self.sysex_buffer.append(self.get_check_sum())
            self.sysex_buffer.append(self.SYSEX_DATA_END)

    def fill_seq_event(self):
        self.build_sysex_buffer()
        if self.is_valid:
            MidiEvent.fill_seq_event(self)
            self.seq_event.set_data({self.SYSEX_DATA_KEY: self.sysex_buffer})

    def get_check_sum(self):
        check_sum = 0
        for data in self.data_buffer:
            check_sum = check_sum ^ data
        return check_sum
