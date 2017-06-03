"""
 gstation-edit PrgChangeEvent definition
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

from gstation_edit.midi.cc_event import CCMidiEvent
from gstation_edit.midi.event_factory import MidiEventFactory

class PrgChangeEvent(CCMidiEvent):
    EVENT_TYPE = alsaseq.SEQ_EVENT_PGMCHANGE

    @classmethod
    def register_event_type_builder(class_):
        MidiEventFactory.register_event_type_builder(PrgChangeEvent)

    @classmethod
    def build_from_seq_event(class_, seq_event):
        return PrgChangeEvent(seq_event=seq_event)
