"""
 gstation-edit SysexMidiEvent definition
"""
# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009-2021 <fengalin@free.fr>
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
from gstation_edit.midi.sysex_buffer import SysexBuffer

class SysexMidiEvent(MidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_SYSEX
    PROCEDURE_ID = 0x00
    PROCEDURE_ID_POS = 0x06

    SYSEX_DATA_KEY = 'ext'
    SYSEX_DATA_START = 0xf0
    SYSEX_DATA_END = 0xf7

    def __init__(self, seq_event=None, sysex_buffer=None):
        MidiEvent.__init__(self, self.EVENT_TYPE, seq_event)

        self.sysex_buffer = sysex_buffer

        if not seq_event is None:
            sysex_data = \
                seq_event.get_data().get(SysexMidiEvent.SYSEX_DATA_KEY)
            if not sysex_data is None:
                self.sysex_buffer = SysexBuffer(sysex_data)
            else:
                self.has_error = True
                print('No data in sysex event')

        if seq_event or sysex_buffer:
            if self.is_valid():
                self.parse_sysex_buffer()
            else:
                self.has_error = True
                print('Invalid sysex buffer => didn\'t parse it')
        else:
            self.fill_seq_event()


    def is_valid(self):
        result = MidiEvent.is_valid(self)
        if not self.sysex_buffer is None:
            result &= self.sysex_buffer.is_valid
        return result

    def get_check_sum(self):
        check_sum = 0
        data_to_check = self.sysex_buffer.get_from_marker()
        for value in data_to_check:
            check_sum = check_sum ^ value
        return check_sum



    def parse_sysex_buffer(self):
        # SysEx data expected structure: 0xf0 ... data ... checksum 0xf7
        if self.sysex_buffer.pop_1_byte() == self.SYSEX_DATA_START:
            self.sysex_buffer.set_marker()

            self.parse_data_buffer()

            if self.is_valid():
                check_sum = self.get_check_sum()
                expected_check_sum = self.sysex_buffer.pop_1_byte()
                if check_sum == expected_check_sum:
                    if self.sysex_buffer.pop_1_byte() != self.SYSEX_DATA_END:
                        self.has_error = True
                        print('Expecting End tag, found x%02x sysex buffer: %s'%(
                                  self.sysex_buffer[self.data_index],
                                  self.sysex_buffer.get_readable_from_marker()
                            )
                        )
                else:
                    self.has_error = True
                    print('Incorrect checksum got: x%02x, expected, x%02x - %s'%(
                        check_sum, expected_check_sum,
                        self.sysex_buffer.get_readable_from_marker())
                    )
                    print('full buffer: %s'%(self.sysex_buffer))


    def parse_data_buffer(self):
        # To be implemented in heirs
        pass

    def read_next_bytes(self, nb_bytes):
        result = self.sysex_buffer.pop_split_bytes(nb_bytes)
        if result == None:
            self.has_error = True
        return result


    # Build to send

    def build_data_buffer(self):
        # To be implemented in heirs
        pass

    def build_sysex_buffer(self):
        self.sysex_buffer = SysexBuffer()
        self.sysex_buffer.push_1_byte(self.SYSEX_DATA_START)
        self.sysex_buffer.set_marker()

        self.build_data_buffer()

        if self.is_valid():
            check_sum = self.get_check_sum()
            self.sysex_buffer.push_raw_bytes([check_sum, self.SYSEX_DATA_END])


    def fill_seq_event(self):
        self.build_sysex_buffer()
        if self.is_valid():
            MidiEvent.fill_seq_event(self)
            self.seq_event.set_data({self.SYSEX_DATA_KEY: self.sysex_buffer.sysex_data})
