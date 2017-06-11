"""
 gstation-edit SplitBytesHelpher definition
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

class SplitBytesHelpher:

    def __init__(self):
        pass

    def get_value_from_split_bytes(self, split_bytes):
        value = None
        if split_bytes != None:
            value = 0
            split_bytes_range = len(split_bytes) / 2
            for index in range(0, split_bytes_range):
                byte_ = split_bytes[2*index + 1]
                if split_bytes[2*index] != 0:
                    byte_ += 0x80
                value = value + (byte_ << (8*index))
        return value

    def get_split_bytes_from_value(self, value, expected_bytes=2):
        split_bytes = list()
        if value >= 0:
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
                if remainder == 0:
                    value_left_to_read = False

        return split_bytes
