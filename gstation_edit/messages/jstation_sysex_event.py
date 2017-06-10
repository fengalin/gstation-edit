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
        if callback:
            MidiEvent.callbacks[class_.__name__] = callback

    @classmethod
    def build_from_seq_event(class_, seq_event):
        result = None
        # assert: seq_event.type == SysExMidiEvent.EVENT_TYPE
        sys_ex_data = seq_event.get_data().get(SysExMidiEvent.SYSEX_DATA_KEY)
        if sys_ex_data:
            if JStationSysExEvent.PROCEDURE_ID_POS < len(sys_ex_data):
                proc_id = sys_ex_data[JStationSysExEvent.PROCEDURE_ID_POS]

                event_class = JStationSysExEvent.event_classes.get(proc_id)
                if event_class:
                    result = event_class(seq_event=seq_event)
                if result == None:
                    result = JStationSysExEvent(seq_event=seq_event)
            else:
                print('Sysex data too short to read procecdure id: %s'\
                      %(sys_ex_data))
        else:
            print('Couldn\'t find sysex data key in seq event: %s'%(seq_event))

        return result


    # constructor
    def __init__(self, channel=-1, seq_event=None, sysex_buffer=None):
        self.manufacturer_id = []
        self.channel = channel
        self.product_id = -1
        self.is_right_product = False

        self.procedure_id = -1
        self.version = -1

        self.data_length = -1

        self.helper = SplitBytesHelpher()
        SysExMidiEvent.__init__(self, seq_event=seq_event,
                                sysex_buffer=sysex_buffer)


    def parse_data_buffer(self, read_len=False):
        if len(self.data_buffer) >= 8:
            self.manufacturer_id = self.data_buffer[:3]
            self.data_index += 3
            self.channel = self.read_next_bytes(1)
            self.product_id = self.read_next_bytes(1)

            self.check_product()
            if self.is_right_product:
                self.procedure_id = self.read_next_bytes(1)
                self.version = self.read_next_bytes(2)

                if type(self) is JStationSysExEvent:
                    # couldn't instantiate a specific class
                    self.is_valid = False
                else:
                    self.is_valid = True
                    if read_len:
                        self.read_data_len()
            else:
                # not a message for us
                self.is_valid = False

        else:
            print('Too short data buffer with len: %d'%(len(self.data_buffer)))
            self.is_valid = False

    def check_product(self):
        self.is_right_product = True
        if self.product_id == self.PRODUCT_ID:
            if len(self.manufacturer_id) == len(self.MANUFACTURER_ID):
                for index in range(0, len(self.MANUFACTURER_ID)):
                    if self.manufacturer_id[index] != self.MANUFACTURER_ID[index]:
                        self.is_right_product = False
                        break
            else:
                self.is_right_product = False
        else:
            self.is_right_product = False

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
        else:
            print('Not enough data to read from data_buffer')
            self.is_valid = False
        return result

    def read_data_len(self):
        self.data_length = self.read_next_bytes(4)
        if len(self.data_buffer) < 2*self.data_length+4:
            self.is_valid = False
            print('Inconsistent data len. Expecting: %d. '\
                  'Received: %d'%(2*self.data_length+4, len(self.data_buffer)))


    # Build to send
    def build_data_buffer(self, pre_len_data=None, post_len_data=None):
        if self.procedure_id == -1:
            self.procedure_id = self.PROCEDURE_ID
        if self.version == -1:
            self.version = self.VERSION

        self.is_right_product = True

        self.data_buffer = list(self.MANUFACTURER_ID)
        self.data_buffer.append(self.channel)
        self.data_buffer.append(self.PRODUCT_ID)
        self.data_buffer.append(self.procedure_id)
        self.data_buffer += \
            self.helper.get_split_bytes_from_value(self.version)

        self.is_valid = True

        if pre_len_data:
            for value in pre_len_data:
                if value >= 0:
                    self.data_buffer += \
                        self.helper.get_split_bytes_from_value(value)
                else:
                    self.is_valid = False
                    self.data_buffer = None
                    break

        if self.is_valid and post_len_data != None:
            self.data_buffer += self.helper.get_split_bytes_from_value(
                    len(post_len_data), 4
                )

            for value in post_len_data:
                if value >= 0:
                    self.data_buffer += \
                        self.helper.get_split_bytes_from_value(value)
                else:
                    self.is_valid = False
                    self.data_buffer = None
                    break


    # Common
    def __str__(self):
        valid = ''
        event_type = 'Uknonw sysex'
        if not type(self) is JStationSysExEvent:
            event_type = self.__class__.__name__
            if self.is_right_product and not self.is_valid:
                valid = ' - not valid'

        prefix = '%s (x%02x)%s. Version: %d'%(event_type,
                                              self.procedure_id & 0xff,
                                              valid,
                                              self.version)
        if not self.is_right_product:
            prefix = 'product: %s/x%02x '\
                %(['x%02x'%(val & 0xff) for val in self.manufacturer_id],
                  self.product_id)

        data = ''
        if self.data_buffer and not self.is_valid:
            data = ', data: %s'%(
                ['x%02x'%(val & 0xff) for val in self.data_buffer[self.data_index:]])

        return '%s%s'%(prefix, data)
