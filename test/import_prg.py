"""
 gstation-edit ImportPrg test
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

import struct

from gstation_edit.midi.sysex_buffer import SysexBuffer

from gstation_edit.messages.one_prg_dump import OneProgramDump

def test():
    print('\n==== ImportPrg test')

    content = None
    # TODO: catch exception and notify to the user
    with open('test/data/Thick Stack Solo.syx', 'rb') as sysex_file:
        content = sysex_file.read()

        sysex_data = list()
        # TODO; use bytes
        byte_content = struct.unpack('B'*len(content), content)
        for value in byte_content:
            sysex_data.append(value)

        one_prg_dump = OneProgramDump(sysex_buffer=SysexBuffer(sysex_data))
        print('one_prg_dump: %s'%one_prg_dump)

