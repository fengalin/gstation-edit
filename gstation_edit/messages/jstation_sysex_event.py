"""
 gstation-edit JStationSysExEvent definition
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

from gstation_edit.midi.event import MidiEvent
from gstation_edit.midi.sysex_event import SysExMidiEvent
from gstation_edit.midi.event_factory import MidiEventFactory
from gstation_edit.midi.split_bytes import SplitBytesHelpher

class JStationSysExEvent(SysExMidiEvent):
    MANUFACTURER_ID = [0, 0, 0x10]
    PRODUCT_ID = 0x54

    ALL_CHANNELS = 0x7e
    MERGE_RESPONSE = 0x7f

    PROCEDURE_ID = -1 # TO BE DEFINED IN HEIRS
    PROCEDURE_ID_POS = 0x06 # in sysex message

    VERSION = -1 # TO BE DEFINED IN HEIRS


    event_classes = dict()

    @classmethod
    def register_event_type_builder(class_):
        MidiEventFactory.register_event_type_builder(JStationSysExEvent)

    @classmethod
    def register(class_, callback=None):
        JStationSysExEvent.event_classes[class_.PROCEDURE_ID] = class_
        if callback != None:
            MidiEvent.callbacks[class_.__name__] = callback

    @classmethod
    def build_from_seq_event(class_, seq_event):
        result = None
        # assert: seq_event.type == SysExMidiEvent.EVENT_TYPE
        sys_ex_data = seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
        if None != sys_ex_data:
            if JStationSysExEvent.PROCEDURE_ID_POS < len(sys_ex_data):
                proc_id = sys_ex_data[JStationSysExEvent.PROCEDURE_ID_POS]

                event_class = JStationSysExEvent.event_classes.get(proc_id)
                if event_class != None:
                    result = JStationSysExEvent.\
                            event_classes[proc_id](seq_event=seq_event)

                if result == None:
                    event = JStationSysExEvent(seq_event=seq_event)
            else:
                print('Sysex data too short to read procecdure id: %s'\
                      %(sys_ex_data))
        else:
            print('Couldn\'t find sysex data key in seq event: %s'%(seq_event))

        return result


    # constructor
    def __init__(self, channel=-1, seq_event=None):
        SysExMidiEvent.__init__(self)
        self.helper = SplitBytesHelpher()

        self.manufacturer_id = []
        self.channel = channel
        self.product_id = -1
        self.procedure_id = -1

        self.data_buffer = list()
        self.data_index = -1
        self.is_valid = False

        if seq_event != None:
            sysex_data = seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
            if None != sysex_data:
                # SysEx data expected structure: 0xf0 ... data ... checksum 0xf7
                len_sysex_data = len(sysex_data)
                if 3 < len_sysex_data:
                    if self.SYSEX_DATA_START == sysex_data[0] and \
                            self.SYSEX_DATA_END == sysex_data[len_sysex_data-1]:
                        # Note: if this first part is common to all sysex
                        # events, it should be moved to SysExMidiEvent along
                        # with the factory stuff above

                        # get the actual buffer and check sum
                        check_sum = sysex_data[len_sysex_data-2]
                        self.data_buffer = sysex_data[1: len_sysex_data-2]
                        self.data_index = 0

                        if check_sum == self.get_check_sum():
                            self.manufacturer_id = self.data_buffer[:3]
                            self.data_index += 3
                            self.channel = self.read_next_bytes(1)
                            self.product_id = self.read_next_bytes(1)
                            self.procedure_id = self.read_next_bytes(1)
                            self.VERSION = self.read_next_bytes(2)
                            if not type(self) is JStationSysExEvent:
                                self.is_valid = True
                            # else: couldn't instantiate a specific class
                        else:
                            print('Incorrect checksum for received sysex')
                            self.is_valid = False
                            self.data_buffer = list()
                    else:
                        print('Incorrect first and/or last byte for SysEx data')
                else:
                    print('Too short length for sysex: %s'%(len_sysex_data))
            else:
                print('Not a sysex event: %d'\
                      %(seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)))


    def read_next_bytes(self, nb_bytes):
        result = None
        if self.data_index+nb_bytes <= len(self.data_buffer):
            if nb_bytes > 1:
                result = self.helper.get_value_from_split_bytes(
                        self.data_buffer[
                            self.data_index:
                            self.data_index+nb_bytes
                        ]
                    )
            else:
                result = self.data_buffer[self.data_index]
            self.data_index += nb_bytes
        return result


    # Build to send
    def build_data_buffer(self, data_before_len=None, data_after_len=None):
        SysExMidiEvent.build_data_buffer(self)
        if -1 != self.PROCEDURE_ID and -1 != self.VERSION:
            self.data_buffer = list(self.MANUFACTURER_ID)
            self.data_buffer.append(self.channel)
            self.data_buffer.append(self.PRODUCT_ID)
            self.data_buffer.append(self.PROCEDURE_ID)
            self.data_buffer += \
                self.helper.get_split_bytes_from_value(self.VERSION)

            if data_before_len != None:
                for value in data_before_len:
                    self.data_buffer += \
                        self.helper.get_split_bytes_from_value(value)

            if data_after_len != None:
                self.data_buffer += self.helper.get_split_bytes_from_value(
                        len(data_after_len), 4
                    )

                for value in data_after_len:
                    self.data_buffer += \
                        self.helper.get_split_bytes_from_value(value)

            self.is_valid = True
        else:
            print('procedure id and/or version not defined for JStationSysEx')
            self.is_valid = False


    # Common
    def __str__(self):
        product = ''
        if self.manufacturer_id != self.MANUFACTURER_ID and \
           self.product_id != self.PRODUCT_ID:
            product = 'product: %s/%d '%(self.manufacturer_id, self.product_id)
        event_type = 'Uknonw sysex'
        valid = ''
        if not type(self) is JStationSysExEvent:
            event_type = self.__class__.__name__
            if not self.is_valid:
                valid = ' - not valid'
        return "%s%s (x%02x)%s. Version: %d"\
                %(product, event_type, self.PROCEDURE_ID, valid, self.VERSION)
