"""
 gstation-edit MidiEventFactory test
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

from gstation_edit.midi.event_factory import *
from gstation_edit.midi.cc_event import *

from gstation_edit.messages.jstation_sysex_event import *
from gstation_edit.messages.who_am_i_resp import *

def test():
    print('\n==== MidiEventFactory test')

    CCMidiEvent.register_event_type_builder()
    CCMidiEvent.register()

    JStationSysExEvent.register_event_type_builder()
    WhoAmIResponse.register()

    sysex_data = [
            0xf0, 0, 0, 0x10, 0x7f, 0x54, 0x41,
            0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 121, 0xf7
        ]
    print('input sysex data: %s'%['x%02x'%(val & 0xff) for val in sysex_data])

    sysex_seq_event = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_SYSEX)
    sysex_evt_data = dict()
    sysex_evt_data['ext'] = sysex_data;
    sysex_seq_event.set_data(sysex_evt_data);

    factory = MidiEventFactory()
    sysex_event = factory.build_from_seq_event(sysex_seq_event)
    if sysex_event:
        print(sysex_event.is_valid())
        print(str(sysex_event))
    else:
        print('sysex not recognised')

    cc_seq_event = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_CONTROLLER)
    cc_data = dict()
    cc_data['control.channel'] = 1;
    cc_data['control.param'] = 34;
    cc_data['control.value'] = 20;
    cc_seq_event.set_data(cc_data);

    cc_event = factory.build_from_seq_event(cc_seq_event)
    if cc_event:
        print(cc_event.is_valid())
        print(str(cc_event))
    else:
        print('cc not recognised')

