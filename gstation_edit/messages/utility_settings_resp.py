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

from jstation_sysex_resp import *

class UtilitySettingsResponse(JStationSysExResponse):
    PROCEDURE_ID = 0x12
    EXPECTED_DATA_LEN = 6
    STEREO_MONO_POS = 12
    DRY_TRACK_POS = 14
    DRY_TRACK_LEVEL_POS = 16
    GLOBAL_CABINET_POS = 18
    MIDI_MERGE_POS = 20
    MIDI_CHANNEL_POS = 22

    def __init__(self, callback=None, seq_event=None):
        JStationSysExResponse.__init__(self, callback, seq_event=seq_event)
        self.stereo_mono = -1
        self.dry_track = -1
        self.dry_track_level = -1
        self.global_cabinet = -1
        self.midi_merge = -1
        self.midi_channel = -1

        if self.is_valid:
            data_length = self.get_count()
            if self.EXPECTED_DATA_LEN == data_length:
                self.stereo_mono = self.get_value_from_split_bytes(
                    self.data_buffer[self.STEREO_MONO_POS : self.STEREO_MONO_POS+2]
                )
                self.dry_track = self.get_value_from_split_bytes(
                    self.data_buffer[self.DRY_TRACK_POS : self.DRY_TRACK_POS+2]
                )
                self.dry_track_level = self.get_value_from_split_bytes(
                    self.data_buffer[self.DRY_TRACK_LEVEL_POS : self.DRY_TRACK_LEVEL_POS+2]
                )
                self.global_cabinet = self.get_value_from_split_bytes(
                    self.data_buffer[self.GLOBAL_CABINET_POS : self.GLOBAL_CABINET_POS+2]
                )
                self.midi_merge = self.get_value_from_split_bytes(
                    self.data_buffer[self.MIDI_MERGE_POS : self.MIDI_MERGE_POS+2]
                )
                self.midi_channel = self.get_value_from_split_bytes(
                    self.data_buffer[self.MIDI_CHANNEL_POS : self.MIDI_CHANNEL_POS+2]
                )
                self.is_valid = True
            else:
                print('Incorrect data length %d within WhoAmIResponse'%(data_length))
                self.m_is_valid = False

    def __str__( self ):
        return "%s. Version: %d, stereo mono: %d, dry track: %d, "\
                "dry track level: %d, global cabinet: %d, "\
                "midi merge: %d, midi channel: %d"%(self.__class__.__name__,
                                                    self.version,
                                                    self.stereo_mono,
                                                    self.dry_track,
                                                    self.dry_track_level,
                                                    self.global_cabinet,
                                                    self.midi_merge,
                                                    self.midi_channel)

