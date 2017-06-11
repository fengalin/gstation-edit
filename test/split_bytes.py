"""
 gstation-edit SplitBytesHelpher test
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

from gstation_edit.midi.split_bytes import *

def print_split_bytes(split_bytes):
    print('%s'%(['x%02x'%val for val in split_bytes]))


def test():
    print('\n==== SplitBytesHelpher test')

    value = 0
    print('Split Bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 123
    print('Split Bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 128 + 123
    print('Split Bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 0x189
    print('Split Bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 0xf089
    print('Split Bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 123
    print('Split Bytes on 4 bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value, 4)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

    value = 4660
    print('Split Bytes on 4 bytes for %d'%(value))
    split_bytes = SplitBytesHelpher.get_split_bytes_from_value(value, 4)
    print_split_bytes(split_bytes)
    print(SplitBytesHelpher.get_value_from_split_bytes(split_bytes))

