"""
 gstation-edit MidiEvent definition
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

class MidiEvent(object):
    # class memeber
    callbacks = dict()

    @classmethod
    def register(class_, callback=None):
        if callback:
            MidiEvent.callbacks[class_.__name__] = callback

    @classmethod
    def is_event(class_, seq_event):
        # implement in heirs
        return False


    def __init__(self, event_type=-1, seq_event=None):
        self.has_error = False
        self.seq_event = seq_event
        if event_type == -1:
            self.event_type = seq_event.type
        else:
            self.event_type = event_type

    def is_valid(self):
        return not self.has_error

    def fill_seq_event(self):
        self.seq_event = alsaseq.SeqEvent(self.event_type)
        # MUST be ovrriden to add specific event data

    def get_seq_event(self):
        if self.is_valid():
            return self.seq_event
        else:
            print('Event is not valid %s'%(self.seq_event))
            self.seq_event = None
            return dict()

    def process(self):
        callback = MidiEvent.callbacks.get(self.__class__.__name__)
        if callback:
            callback(self)
        else:
            print('Couldn\'t find callback for %s'%(self.__class__.__name__))

