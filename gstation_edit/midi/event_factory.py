"""
 gstation-edit MidiEventFactory definition
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

class MidiEventFactory:
    event_type_builder_classes = dict()

    def __init__(self):
        pass

    @classmethod
    def register_event_type_builder(self_class, event_type_class):
#        print('Registering MIDI  event type builder: %s'%(event_type_class))
        MidiEventFactory.event_type_builder_classes[
                event_type_class.EVENT_TYPE.real
            ] = event_type_class


    @classmethod
    def build_from_seq_event(class_, seq_event):
        result = None
        if seq_event:
#            print('Received event with type %d'%(seq_event.type))
            event_type_builder = MidiEventFactory.\
                event_type_builder_classes.get(seq_event.type.real)
            if event_type_builder:
                result = event_type_builder.build_from_seq_event(seq_event)
                if result:
#                    print('Event identified as: %s'%(result))
                    pass
                else:
                    print('Couldn\'t identify event: %s'%(seq_event))
            else:
                print('Unknown event type for: %s'%(seq_event))
        return result
