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
from gstation_edit.midi.sysex_event import SysexMidiEvent
from gstation_edit.midi.event_factory import MidiEventFactory

class JStationSysExEvent(SysexMidiEvent):
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
        sys_ex_data = seq_event.get_data().get(SysexMidiEvent.SYSEX_DATA_KEY)
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

        SysexMidiEvent.__init__(self, seq_event=seq_event,
                                sysex_buffer=sysex_buffer)


    def parse_data_buffer(self):
        self.manufacturer_id = self.sysex_buffer.pop_raw_bytes(3)
        self.channel = self.sysex_buffer.pop_1_byte()
        self.product_id = self.sysex_buffer.pop_1_byte()

        if self.is_valid():
            self.check_product()
            if self.is_valid() and self.is_right_product:
                self.procedure_id = self.sysex_buffer.pop_1_byte()
                if self.procedure_id == self.PROCEDURE_ID:
                    self.version = self.read_next_bytes(2)

                    if type(self) is JStationSysExEvent:
                        # couldn't instantiate a specific class
                        # this is used to trace events which are not implemented yet
                        self.has_error = True
                else:
                    self.has_error = True
                    print('Received proc id: x%02x, expected: x%02x'%(
                           self.procedure_id, self.PROCEDURE_ID)
                    )
            else:
                # not a message for us
                self.has_error = True
                print('Received a message for product: %s/x%02x '\
                    %(['x%02x'%(val & 0xff) for val in self.manufacturer_id],
                      self.product_id)
                )
        else:
            print('Message is invalid')


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


    # Build to send
    def build_data_buffer(self, pre_len_data=None, post_len_data=None):
        if self.procedure_id == -1:
            self.procedure_id = self.PROCEDURE_ID
        if self.version == -1:
            self.version = self.VERSION

        self.is_right_product = True

        self.sysex_buffer.push_raw_bytes(self.MANUFACTURER_ID)
        self.sysex_buffer.push_raw_bytes([
            self.channel, self.PRODUCT_ID, self.procedure_id
        ])
        self.sysex_buffer.push_as_split_bytes(self.version)

        if pre_len_data:
            for value in pre_len_data:
                if value >= 0:
                    self.sysex_buffer.push_as_split_bytes(value)
                else:
                    self.has_error = True
                    break

        if self.is_valid() and post_len_data != None:
            self.sysex_buffer.push_as_split_bytes(len(post_len_data), 4)

            for value in post_len_data:
                if value >= 0:
                    self.sysex_buffer.push_as_split_bytes(value)
                else:
                    self.has_error = True
                    break


    # Common
    def __str__(self):
        valid = ''
        event_type = 'Uknonw sysex'
        if not type(self) is JStationSysExEvent:
            event_type = self.__class__.__name__
            if self.is_right_product and not self.is_valid():
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
        if self.sysex_buffer.data_len > 0 and not self.is_valid():
            data = ', sysex: %s'%(self.sysex_buffer)

        return '%s%s'%(prefix, data)
