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

from gstation_edit.midi.event import MidiEvent
from gstation_edit.midi.event_factory import MidiEventFactory

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

        if seq_event:
            seq_event_data = seq_event.get_data()
            value = seq_event_data.get(self.PARAM_KEY)
            if value:
                self.param = value

            value = seq_event_data.get(self.CHANNEL_KEY)
            if value:
                self.channel = value

            value = seq_event_data.get(self.VALUE_KEY)
            if value:
                self.value = value

            if self.param == -1 and self.channel == -1 and self.value == -1:
                self.has_error = True
        else:
            self.fill_seq_event()


    def fill_seq_event(self):
        MidiEvent.fill_seq_event(self)
        if self.channel >= 0:
            event_data = dict()
            if self.param >= 0:
                event_data[self.PARAM_KEY] = self.param
            event_data[self.CHANNEL_KEY] = self.channel
            if self.value >= 0:
                event_data[self.VALUE_KEY] = self.value
            self.seq_event.set_data(event_data)


    def __str__(self):
        param = ''
        if self.param >= 0:
            param = ', param: %d'%(self.param)
        value = ''
        if self.value >= 0:
            value = ', value: %d'%(self.value)
        return '%s. channel: %d%s%s'%(self.__class__.__name__,
                                      self.channel, param, value)

