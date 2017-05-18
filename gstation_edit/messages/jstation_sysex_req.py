"""
 gstation-edit JStationSysExRequest definition
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

from ..midi.sysex_event import *

class JStationSysExRequest(SysExMidiEvent):
    MANUFACTURER_ID = [0, 0, 0x10]
    PRODUCT_ID = 0x54

    ALL_CHANNELS = 0x7e
    MERGE_RESPONSE = 0x7f

    def __init__(self, channel_id=-1, procedure_id=0, version=0):
        SysExMidiEvent.__init__(self)
        self.channel_id = channel_id
        self.procedure_id = procedure_id
        self.version = version

    def build_data_buffer(self):
        SysExMidiEvent.build_data_buffer(self)
        if -1 != self.procedure_id and -1 != self.version:
            self.data_buffer = list(self.MANUFACTURER_ID)
            self.data_buffer.append(self.channel_id)
            self.data_buffer.append(self.PRODUCT_ID)
            self.data_buffer.append(self.procedure_id)
            self.data_buffer = self.data_buffer \
                               + self.get_split_bytes_from_value(self.version)
            self.is_valid = True
        else:
            print('procedure id and/or version not defined for JStationSysEx')
            self.is_valid = False

    def get_sysex_buffer(self, data):
        sysex_buffer = list()
        sysex_buffer += self.get_split_bytes_from_value(len(data), 4)
        for value in data:
            sysex_buffer += self.get_split_bytes_from_value(value)
        return sysex_buffer
