"""
 gstation-edit UtilitySettingsResponse definition
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

from gstation_edit.messages.jstation_sysex_event import JStationSysExEvent

class UtilitySettingsResponse(JStationSysExEvent):
    PROCEDURE_ID = 0x12
    VERSION = 1

    def __init__(self, channel=-1, seq_event=None,
                 stereo_mono=-1, dry_track=-1, digital_out_level=-1,
                 global_cabinet=-1, midi_merge=-1, midi_channel=-1):
        self.stereo_mono = stereo_mono
        self.dry_track = dry_track
        self.digital_out_level = digital_out_level
        self.global_cabinet = global_cabinet
        self.midi_merge = midi_merge
        self.midi_channel = midi_channel

        JStationSysExEvent.__init__(self, channel, seq_event=seq_event)


    def parse_data_buffer(self):
        JStationSysExEvent.parse_data_buffer(self)
        data_len = self.read_next_bytes(4)

        if self.is_valid():
            if data_len == 6:
                self.stereo_mono = self.read_next_bytes(2)
                self.dry_track = self.read_next_bytes(2)
                self.digital_out_level = self.read_next_bytes(2)
                self.global_cabinet = self.read_next_bytes(2)
                self.midi_merge = self.read_next_bytes(2)
                self.midi_channel = self.read_next_bytes(2)
            else:
                print('UtilitySettingsResponse: data len error: '\
                      'got %d expected 6'%(data_len))


    # Build to send
    def build_data_buffer(self):
        data = list()
        data.append(self.stereo_mono)
        data.append(self.dry_track)
        data.append(self.digital_out_level)
        data.append(self.global_cabinet)
        data.append(self.midi_merge)
        data.append(self.midi_channel)

        JStationSysExEvent.build_data_buffer(self, post_len_data=data)


    def __str__( self ):
        return '%s, stereo mono: %d, dry track: %d, '\
               'digital out level: %d, global cabinet: %d, '\
               'midi merge: %d, midi channel: %d'\
               %(JStationSysExEvent.__str__(self),
                 self.stereo_mono, self.dry_track,
                 self.digital_out_level, self.global_cabinet,
                 self.midi_merge, self.midi_channel)

