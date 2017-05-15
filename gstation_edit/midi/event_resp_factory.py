"""
 gstation-edit MidiEventResponseFactory definition
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

from event import *

class MidiEventResponseFactory:
    event_classes = list()

    def __init__(self):
        pass

    def register_midi_event(self_class, midi_event_class, bases):
#        print('Registering: %s'%(midi_event_class))
        self_class.event_classes.append(midi_event_class)
    register_midi_event = classmethod(register_midi_event)

    def get_event_from_seq_event(self, seq_event):
        result = None
        if None != seq_event:
#            print('Received event with type %d'%(seq_event.type))
            for event_class in self.event_classes:
                    if event_class.is_event(seq_event):
#                        print('Event recognized as: %s'%(l_event_class.__name__))
                        result = event_class(seq_event=seq_event)
                        break
        return result
