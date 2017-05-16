"""
 gstation-edit JStationInterface definition
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

from midi.port import *
from midi.event_resp_factory import *
from midi.cc_event import *
from midi.prg_change_event import *

from messages.who_am_i_req import *
from messages.utility_settings_req import *
from messages.bank_dump_req import *
from messages.receive_prg_update_req import *
from messages.request_prg_update_req import *

from messages.who_am_i_resp import *
from messages.utility_settings_resp import *
from messages.start_bank_dump_resp import *
from messages.prg_indices_resp import *
from messages.one_prg_resp import *
from messages.end_bank_dump_resp import *
from messages.to_msg_resp import *
from messages.receive_prg_update_resp import *

class JStationInterface:
    WAIT_SHUTDOWN_TIMEOUT = 1000 # ms - this one determines the longest period
                                 #            before a shudown request can be detected
    RESPONSE_TIMEOUT = 2 # s

    def __init__(self, rack):
        # instanciate response events in order for them to be available to the factory
        # and define the callback function for processing
        CCMidiEvent(callback=self.one_parameter_cc_callback)
        PrgChangeEvent(callback=self.program_change_callback )
        WhoAmIResponse(callback=self.who_am_i_callback)
        UtilitySettingsResponse(callback=self.utility_settings_callback)
        StartBankDumpResponse(callback=self.default_event_callback)
        PRGIndicesResponse(callback=self.program_indices_callback)
        OneProgramResponse(callback=self.one_program_callback)
        EndBankDumpResponse(callback=self.end_bank_dump_callback)
        ToMessageResponse(callback=self.response_to_message_callback)
        ReceiveProgramUpdateResponse(callback=self.program_update_response)

        self.is_connected = False
        self.is_disconnecting = Event()
        self.is_response_received_cndt = Condition()

        self.receive_channel = -1
        self.sysex_channel = -1

        self.js_port_in = None
        self.js_port_out = None

        self.jstation_wait_for_events_thread = None


        self.rack = rack
        self.is_disconnecting.clear()

        self.seq = alsaseq.Sequencer('hw',
                                     'gstation-edit',
                                     alsaseq.SEQ_OPEN_DUPLEX,
                                     alsaseq.SEQ_NONBLOCK, 1)
        if self.seq == None:
            print('Error while opening sequencer')
            exit(1)

        self.get_clients()

        self.port_out = self.seq.create_simple_port(
            'Output',
            alsaseq.SEQ_PORT_CAP_READ | alsaseq.SEQ_PORT_CAP_SUBS_READ
        )
        self.port_in = self.seq.create_simple_port(
            'Input',
            alsaseq.SEQ_PORT_TYPE_APPLICATION,
            alsaseq.SEQ_PORT_CAP_WRITE | alsaseq.SEQ_PORT_CAP_SUBS_WRITE
        )


    def get_clients(self):
        connections = self.seq.connection_list()
        self.midi_in_ports = list()
        self.midi_out_ports = list()

        for (cname, cid, ports) in connections:
            for port in ports:
                port_name, port_id, port_connections = port
                port_info = self.seq.get_port_info(port_id, cid)
                if port_info['type'] & alsaseq.SEQ_PORT_TYPE_PORT:
                    port_cap = port_info['capability']
                    if port_cap & alsaseq.SEQ_PORT_CAP_SUBS_READ:
                        self.midi_in_ports.append(MidiPort(cid, port_id, port_name))
                    if port_cap & alsaseq.SEQ_PORT_CAP_WRITE:
                        self.midi_out_ports.append(MidiPort(cid, port_id, port_name))


    def connect(self, midi_port_in, midi_port_out, sysex_channel):
        self.is_connected = False
        self.sysex_channel = sysex_channel
        self.js_port_in = midi_port_in
        self.seq.connect_ports(
            (self.seq.client_id, self.port_out),
            (midi_port_in.client, midi_port_in.port)
        )
        connect_info = self.seq.get_connect_info(
            (self.seq.client_id, self.port_out),
            (midi_port_in.client, midi_port_in.port)
        )
        self.js_port_out = midi_port_out
        self.seq.connect_ports(
            (midi_port_out.client, midi_port_out.port),
            (self.seq.client_id, self.port_in)
        )
        connect_info = self.seq.get_connect_info(
            (midi_port_out.client, midi_port_out.port),
            (self.seq.client_id, self.port_in)
        )

        self.is_response_received_cndt.acquire()
        self.jstation_wait_for_events_thread = Thread(
            target = self.wait_for_events,
            name = 'wait for events'
        )
        self.jstation_wait_for_events_thread.start()
        self.send_event(WhoAmIRequest())

        self.is_response_received_cndt.wait(self.RESPONSE_TIMEOUT)
        self.is_response_received_cndt.release()

        if not self.is_connected:
            self.disconnect()
        else:
            self.is_response_received_cndt.acquire()
            self.send_event(UtilitySettingsRequest(self.sysex_channel))
            self.is_response_received_cndt.wait(self.RESPONSE_TIMEOUT)
            self.is_response_received_cndt.release()


    def disconnect(self):
        self.is_disconnecting.set()
        if None != self.jstation_wait_for_events_thread:
            # wait until waiting thread is terminated
            self.jstation_wait_for_events_thread.join()
            self.jstation_wait_for_events_thread = None

        if None != self.js_port_in:
            self.seq.disconnect_ports(
                (self.seq.client_id, self.port_out),
                (self.js_port_in.client, self.js_port_in.port)
            )
        if None != self.js_port_out:
            self.seq.disconnect_ports(
                (self.js_port_out.client, self.js_port_out.port),
                (self.seq.client_id, self.port_in)
            )
        self.js_port_in = None
        self.js_port_out = None
        self.is_connected = False
        self.is_disconnecting.clear()


    def req_bank_dump(self):
        if self.is_connected:
            self.send_event(BankDumpRequest(self.sysex_channel))
        else:
            print('req_bank_dump canceled: not connected')

    def req_program_update_req(self):
        # TODO: find out the exact meaning since the name is too close to the next one
        if self.is_connected:
            self.send_event(RequestProgramUpdateRequest(self.sysex_channel))
        else:
            print('req_program_update_req canceled: not connected')

    def req_program_update(self, program):
        if self.is_connected:
            self.is_response_received_cndt.acquire()
            self.send_event(ReceiveProgramUpdateRequest(program, self.sysex_channel))
            self.is_response_received_cndt.wait(self.RESPONSE_TIMEOUT)
            self.is_response_received_cndt.release()
        else:
            print('req_program_update: not connected')

    def req_program_change(self, program_nb):
        if self.is_connected:
            # TODO: parameter is not set for PrgChangeEvent =>
            #       maybe CCMidiEvent and PrgChangeEvent classes should be swapped
            self.send_event(PrgChangeEvent(self.receive_channel, 0, program_nb))
        else:
            print('req_program_change: not connected')


    def wait_for_events(self):
        event_list = list()
        while not self.is_disconnecting.is_set():
            event_list = self.seq.receive_events(self.WAIT_SHUTDOWN_TIMEOUT, 1)
            if 0 < len(event_list):
                for seq_event in event_list:
                    if None != seq_event:
#                        print('response from JStation: %s'%(seq_event))
                        factory = MidiEventResponseFactory()
                        event = factory.get_event_from_seq_event(seq_event)
                        if None != event:
                            event.process()
                        else:
                            print('could not build event from response')
                    else:
                        print('seq event is null')
                event_list = list()
            # else: no response received (timed out)

    def default_event_callback(self, event):
        if event.is_valid:
#            print('==> received %s'%(event))
            pass
        else:
            print('event is invalid %s'(event))

    def who_am_i_callback(self, event):
        self.default_event_callback(event)
        self.is_response_received_cndt.acquire()
        self.receive_channel = event.receive_channel
        self.sysex_channel = event.sysex_channel
        self.is_connected = True
        self.is_response_received_cndt.notify()
        self.is_response_received_cndt.release()
        print('Found JStation on input %s and output %s '\
              %(str(self.js_port_in ), str( self.js_port_out)))

    def utility_settings_callback(self, event):
        self.default_event_callback(event)
        self.is_response_received_cndt.acquire()
        self.receive_channel = event.midi_channel
        # TODO: feedback to the UI
        self.is_response_received_cndt.notify()
        self.is_response_received_cndt.release()

    def program_indices_callback(self, event):
        self.default_event_callback(event)
        if None != self.rack:
            self.rack.set_program_count(len(event.prg_indices))

    def one_program_callback(self, event):
        self.default_event_callback(event)
        if None != self.rack:
            self.rack.receive_program_from_jstation(event.prg)

    def end_bank_dump_callback(self, event):
        self.default_event_callback(event)
        thread = Thread(target=self.req_program_update_req, name='send req prg up')
        thread.start()

    def one_parameter_cc_callback( self, event):
        self.default_event_callback(event)
        if None != self.rack:
            self.rack.update_parameter_from_jstation(event.param,
                                                     event.value,
                                                     is_cc=True)

    def program_change_callback(self, event):
        self.default_event_callback(event)
        if None != self.rack:
            self.rack.select_program_from_its_number(event.value)

    def program_update_response(self, event):
        self.default_event_callback(event)
        if None != self.rack:
            # TODO: handle has changed also
            self.rack.select_program_from_its_content(event.prg)

    def response_to_message_callback(self, event):
        self.is_response_received_cndt.acquire()
        self.default_event_callback(event)
        self.is_response_received_cndt.notify()
        self.is_response_received_cndt.release()
        if 0 != event.error_code:
            print('Received error: %s'%(event))

    def send_event(self, event):
        success = False
        event.fill_seq_event()
        if event.is_valid:
#            print('<== sending %s'%(event.get_seq_event()))
            self.seq.output_event(event.get_seq_event())
            self.seq.drain_output()
#            print('...sent')
            success = True
        else:
            print('failed to build seq event for: %s'%(event))
        return success

    def send_command(self, command, value):
        success = False
        return self.send_event(CCMidiEvent(self.receive_channel, command, value))

if __name__ == '__main__':
    jstation_interface = JStationInterface(None)
    jstation_interface.get_clients()
    for midi_port in jstation_interface.midi_in_ports:
        print(midi_port)
    for midi_port in jstation_interface.midi_out_ports:
        print(midi_port)
