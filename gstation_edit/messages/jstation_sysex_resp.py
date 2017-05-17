"""
 gstation-edit JStationSysExResponse definition
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
# with this program.    If not, see <http://www.gnu.org/licenses/>.

from gstation_edit.midi.sysex_event import *
from gstation_edit.midi.event_resp_factory import *


class JStationSysExResponse(SysExMidiEvent):
    PROCEDURE_ID = 0x00
    PROCEDURE_ID_POS = 0x06

    COUNT_POS = 0x08
    VERSION_POS = 0x06
    VERSION_POS_END = 0x08

    # class memeber
    callbacks = dict()

    class __metaclass__(type):
        def __init__(class_, name, bases, dict):
            if name != 'JStationSysExResponse':
                MidiEventResponseFactory.register_midi_event(class_, bases)

    def is_event(class_, seq_event):
        result = False
        if SysExMidiEvent.EVENT_TYPE == seq_event.type:
            sys_ex_data = seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
            if None != sys_ex_data:
                if class_.PROCEDURE_ID_POS < len(sys_ex_data):
                    if class_.PROCEDURE_ID == \
                            sys_ex_data[JStationSysExResponse.PROCEDURE_ID_POS]:
                        # matching procedure id
                        #print("%s: found matching procecdure id"%(class_))
                        result = True
                    else:
                        #print("%s: procecdure id msimatch: %d / %d"\
                        #      %(class_,
                        #        sys_ex_data[JStationSysExResponse.PROCEDURE_ID_POS],
                        #        class_.PROCEDURE_ID))
                        pass
                else:
                    #print("%s: sysex data too short to read procecdure id"%(class_))
                    pass
            else:
                #print("%s: couldn't sysex data key: %d"%(class_))
                pass
        else:
            #print("%s: doesn't match event with type: %d"%(class_,
            #                                               seq_event.type))
            pass
        return result
    is_event = classmethod(is_event)

    def __init__(self, callback=None, seq_event=None):
        SysExMidiEvent.__init__(self, seq_event)
        self.version = -1

        if None != callback:
            # add to the class member dict for callbacks
            self.callbacks[self.__class__.__name__] = callback

        if None != seq_event:
            sysex_data = seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
            if None != sysex_data:
                # SysEx data expected structure: 0xf0 ... data ... checksum 0xf7
                len_sysex_data = len(sysex_data)
                if 3 < len_sysex_data:
                    if self.SYSEX_DATA_START == sysex_data[0] and \
                            self.SYSEX_DATA_END == sysex_data[len_sysex_data-1]:
                        # get the actual buffer and check sum
                        self.data_buffer = list()
                        self.data_buffer = sysex_data[1 : len_sysex_data-2]
                        check_sum = sysex_data[len_sysex_data-2]
                        if check_sum == self.get_check_sum():
                            if self.VERSION_POS_END <= len(self.data_buffer):
                                self.version = self.get_value_from_split_bytes(
                                    self.data_buffer[self.VERSION_POS:
                                                     self.VERSION_POS_END
                                    ]
                                )
                                self.is_valid = True
                            else:
                                print('Data buffer is too short to get response''s version')
                                self.is_valid = False
                        else:
                            print('Incorrect checksum for received sysex')
                            self.is_valid = False
                            self.data_buffer = list()
                    else:
                        print('Incorrect first and/or last byte for SysEx data')
                else:
                    print('Too short length for sysex: ' + len_sysex_data)

    def get_count(self, count_pos = COUNT_POS):
        count_value = -1
        if self.COUNT_POS + 2 <= len(self.data_buffer):
            count = self.data_buffer[count_pos : count_pos+2]
            count_value = self.get_value_from_split_bytes(count)
        else:
            print('Incompatible size for data_buffer if count is to be retrieved')
        return count_value

    def process(self):
        callback = self.callbacks.get(self.__class__.__name__)
        if None != callback:
            callback(self)
        else:
            print('Couldn''t find callback for %s'%(self.__class__.__name__))

