"""
 gstation-edit CCMidiEvent definition
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

from pyalsa import alsaseq

from .event import *
from .event_factory import *

class CCMidiEvent(MidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_CONTROLLER
    CHANNEL_KEY = 'control.channel'
    PARAM_KEY = 'control.param'
    VALUE_KEY = 'control.value'

    @classmethod
    def register_event_type_builder(class_):
        MidiEventFactory.register_event_type_builder(CCMidiEvent)

    @classmethod
    def build_from_seq_event(class_, seq_event):
        return CCMidiEvent(seq_event=seq_event)


    def __init__(self, channel=-1, param=-1, value=-1, seq_event=None):
        MidiEvent.__init__(self, self.EVENT_TYPE, seq_event)

        self.channel = channel
        self.param = param
        self.value = value

        if seq_event != None:
            error_msg = ''

            seq_event_data = seq_event.get_data()
            value = seq_event_data.get(self.PARAM_KEY)
            if None != value :
                self.param = value

            value = seq_event_data.get(self.CHANNEL_KEY)
            if None != value :
                self.channel = value
            else:
                error_msg += 'Could not find key %s. '%(self.CHANNEL_KEY)

            value = seq_event_data.get(self.VALUE_KEY)
            if None != value :
                self.value= value
            else:
                error_msg += 'Could not find key %s. '%(self.VALUE_KEY)

            if 0 < len(error_msg):
                print(error_msg)
                self.is_valid = False
            else:
                self.is_valid = True


    def fill_seq_event(self):
        MidiEvent.fill_seq_event(self)
        if 0 <= self.channel and 0 <= self.value:
            event_data = dict()
            if self.param >= 0:
                event_data[self.PARAM_KEY] = self.param
            event_data[self.CHANNEL_KEY] = self.channel
            event_data[self.VALUE_KEY] = self.value
            self.seq_event.set_data(event_data)
            self.is_valid = True

    def __str__(self):
        param = ''
        if self.param >= 0:
            param = ' param: %d,'%(self.param)
        return "%s. channel: %d,%s value: %d"%(self.__class__.__name__,
                                                        self.channel,
                                                        param,
                                                        self.value)

