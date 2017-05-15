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

from event import *
from event_resp_factory import *

class CCMidiEvent(MidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_CONTROLLER
    CHANNEL_KEY = 'control.channel'
    PARAM_KEY = 'control.param'
    VALUE_KEY = 'control.value'

    # class memeber
    callbacks = dict()

    class __metaclass__(type):
        def __init__(class_, name, bases, dict):
            MidiEventResponseFactory.register_midi_event(class_, bases)

    def is_event(class_, seq_event):
        result = False
        if class_.EVENT_TYPE == seq_event.type:
            result = True
        return result
    is_event = classmethod(is_event)

    def __init__(self, channel=-1, param=-1, value=-1,
                 callback=None, seq_event=None):
        MidiEvent.__init__(self, self.EVENT_TYPE, seq_event)

        self.channel = -1
        self.param = -1
        self.value = -1

        if None != callback:
            # add to the class member dict for callbacks
            self.callbacks[self.__class__.__name__] = callback
        if None != seq_event:
            error_msg = ''

            seq_event_data = seq_event.get_data()
            value = seq_event_data.get(self.CHANNEL_KEY)
            if None != value :
                self.channel = value
            else:
                error_msg += 'Could not find key %s. '%(self.CHANNEL_KEY)

            value = seq_event_data.get(self.PARAM_KEY)
            if None != value :
                self.param = value
            else:
                error_msg += 'Could not find key %s. '%(self.PARAM_KEY)

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
        else:
            self.channel = channel
            self.param = param
            self.value = value


    def fill_seq_event(self):
        MidiEvent.fill_seq_event(self)
        if 0 <= self.channel and 0 <= self.param and 0 <= self.value:
            event_data = dict()
            event_data[self.CHANNEL_KEY] = self.channel
            event_data[self.PARAM_KEY] = self.param
            event_data[self.VALUE_KEY] = self.value
            self.seq_event.set_data(event_data)
            self.is_valid = True

    def process(self):
        callback = self.callbacks.get(self.__class__.__name__)
        if None != callback:
            callback(self)

    def __str__(self):
        return "%s. channel: %d, param: %d, value: %d"%(self.__class__.__name__,
                                                        self.channel,
                                                        self.param,
                                                        self.value)

