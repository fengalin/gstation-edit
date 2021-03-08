"""
 gstation-edit JStationSniffer definition
"""
# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009-2021 <fengalin@free.fr>
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

from threading import Thread, Event, Condition

from pyalsa import alsaseq

from gstation_edit.jstation_interface import JStationInterface


class JStationSniffer(JStationInterface):
    def __init__(self, app_name):
        JStationInterface.__init__(self, app_name, None)


    def start_sniffer(self):
        # Note: connection to J-Station must have been established
        # using connect()
        if not self.is_connected:
            print('Establish connection to J-Station first')
            return

        self.is_disconnecting.set()
        if self.jstation_wait_for_events_thread:
            # wait until waiting thread is terminated
            self.jstation_wait_for_events_thread.join()
            self.jstation_wait_for_events_thread = None
            self.is_disconnecting.clear()
            print('Terminated J-Station connection event loop')

        print('\nSniffing events...')
        self.jstation_wait_for_events_thread = Thread(
            target = self.sniff_events,
            name = 'sniff events'
        )
        self.jstation_wait_for_events_thread.start()

    def sniff_events(self):
        jstation_cid = self.js_port_out.client
        jstation_in_port = self.js_port_in.port
        event_list = list()
        while not self.is_disconnecting.is_set():
            event_list = self.seq.receive_events(self.WAIT_SHUTDOWN_TIMEOUT, 1)
            for seq_event in event_list:
                if not seq_event is None:
                    forward_event = False
                    origin = 'J-Station'
                    source_cid, source_port = seq_event.source
                    if source_cid != jstation_cid:
                        origin = 'J-Edit'
                        forward_event = True

                    event = self.factory.build_from_seq_event(seq_event)
                    if not event is None:
                        print('\n- **%s** => %s'%(origin, event))
                    else:
#                            print('\n** Could not build event')
                        pass

                    if forward_event:
                        seq_event.dest = (jstation_cid, jstation_in_port)
                        self.seq.output_event(seq_event)
                        self.seq.drain_output()
                else:
                    print('seq event is null')
            event_list = list()

