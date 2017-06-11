"""
 gstation-edit SysexBuffer definition
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

from gstation_edit.midi.split_bytes import SplitBytesHelpher

class SysexBuffer():

    def __init__(self, sysex_data=None):
        self.sysex_data = sysex_data
        self.data_len = -1
        self.data_index = -1
        self.marker = -1
        self.is_valid = False

        if sysex_data:
            self.data_len = len(sysex_data)
            self.data_index = 0
            self.is_valid = True

    def set_marker(self):
        self.marker = self.data_index

    def get_from_marker(self):
        return self.sysex_data[self.marker: self.data_index]

    def get_readable_from_marker(self):
        extract = self.sysex_data[self.marker: self.data_index]
        return 'index: %d/%d\n\t%s'%(
                self.data_index-self.marker, len(extract),
                ['x%02x'%(val & 0xff) for val in extract]
            )


    def has_more(self):
        return self.data_index < self.data_len

    def rewind(self):
        self.data_index = 0
        self.marker = -1


    def pop_raw_bytes(self, nb_bytes):
        result = None
        if self.data_index+nb_bytes <= self.data_len:
            end_pos = self.data_index + nb_bytes
            result = self.sysex_data[self.data_index: end_pos]
            self.data_index = end_pos
        else:
            print('Not enough data to read from sysex_buffer: %s'%(self))
            self.is_valid = False
        return result

    def pop_1_byte(self):
        result = self.pop_raw_bytes(1)
        if result != None:
            result = result[0]
        return result

    def pop_split_bytes(self, nb_bytes):
        result = None
        raw_bytes = self.pop_raw_bytes(nb_bytes)
        result = SplitBytesHelpher.get_value_from_split_bytes(raw_bytes)
        return result



    def push_raw_bytes(self, raw_bytes):
        if not self.is_valid:
            self.sysex_data = list()
            self.data_index = 0
            self.data_len = 0
            self.is_valid = True
        self.sysex_data += raw_bytes
        self.data_index += len(raw_bytes)
        self.data_len += len(raw_bytes)

    def push_1_byte(self, raw_byte):
        self.push_raw_bytes([raw_byte])

    def push_as_split_bytes(self, value, expected_bytes=2):
        raw_bytes = \
            SplitBytesHelpher.get_split_bytes_from_value(value, expected_bytes)
        self.push_raw_bytes(raw_bytes)


    def append(self, other):
        self.push_raw_bytes(other.sysex_data)


    def __str__(self):
        return 'index: %d/%d\n\t%s'%(
                self.data_index, self.data_len,
                ['x%02x'%(val & 0xff) for val in self.sysex_data]
            )
