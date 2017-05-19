"""
 gstation-edit JStationSniffer definition
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

from threading import Thread, Event, Condition
import select

from gstation_edit.jstation_interface import *

class JStationSniffer(JStationInterface):
    def __init__(self):
        JStationInterface.__init__(self, None)


    def connect_sniffer(self, midi_port_in, midi_port_out):
        # Note: connection to J-Station must have been established
        # using connect()
        if self.is_connected:
            self.is_disconnecting.set()
            if None != self.jstation_wait_for_events_thread:
                # wait until waiting thread is terminated
                self.jstation_wait_for_events_thread.join()
                self.jstation_wait_for_events_thread = None
                self.is_disconnecting.clear()
                print('terminated j-station connection event loop')

            print('\nLaunching sniffer event loop')
            self.jstation_wait_for_events_thread = Thread(
                target = self.sniff_events,
                name = 'sniff events'
            )
            self.jstation_wait_for_events_thread.start()
        else:
            print('Establish connection to J-Station first')


    def sniff_events(self):
        event_list = list()
        while not self.is_disconnecting.is_set():
            event_list = self.seq.receive_events(self.WAIT_SHUTDOWN_TIMEOUT, 1)
            if 0 < len(event_list):
                for seq_event in event_list:
                    if None != seq_event:
                        print('==> Received event: %s'%(seq_event))
                        factory = MidiEventResponseFactory()
                        event = factory.get_event_from_seq_event(seq_event)
                        if None != event:
                            print('Event recognized as: %s'%(event))
                        else:
                            print('could not build event from response')
                    else:
                        print('seq event is null')
                event_list = list()
            # else: no response received (timed out)

