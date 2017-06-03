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

from threading import Thread, Event, Condition

from pyalsa import alsaseq

from gstation_edit.midi.port import MidiPort
from gstation_edit.midi.event_factory import MidiEventFactory
from gstation_edit.midi.cc_event import CCMidiEvent
from gstation_edit.midi.prg_change_event import PrgChangeEvent


from gstation_edit.messages.jstation_sysex_event import JStationSysExEvent
from gstation_edit.messages.program import Program

from gstation_edit.messages.bank_dump_req import BankDumpRequest
from gstation_edit.messages.end_bank_dump_resp import EndBankDumpResponse

from gstation_edit.messages.notify_store import NotifyStore
from gstation_edit.messages.notify_utility import NotifyUtility

from gstation_edit.messages.one_prg_req import OneProgramRequest
from gstation_edit.messages.one_prg_resp import OneProgramResponse

from gstation_edit.messages.prg_indices_req import PRGIndicesRequest
from gstation_edit.messages.prg_indices_resp import PRGIndicesResponse

from gstation_edit.messages.receive_prg_update import ReceiveProgramUpdate
from gstation_edit.messages.reload_prg import ReloadProgram
from gstation_edit.messages.request_prg_update import RequestProgramUpdate

from gstation_edit.messages.start_bank_dump_resp import StartBankDumpResponse

from gstation_edit.messages.to_msg_resp import ToMessageResponse

from gstation_edit.messages.utility_settings_req import UtilitySettingsRequest
from gstation_edit.messages.utility_settings_resp import UtilitySettingsResponse

from gstation_edit.messages.who_am_i_req import WhoAmIRequest
from gstation_edit.messages.who_am_i_resp import WhoAmIResponse


class JStationInterface:
    WAIT_SHUTDOWN_TIMEOUT = 1000 # ms - this one determines the longest period
                                 #            before a shudown request can be detected
    RESPONSE_TIMEOUT = 2 # s

    def __init__(self, app_name, main_window):
        self.factory = MidiEventFactory()

        CCMidiEvent.register_event_type_builder()
        CCMidiEvent.register(self.one_parameter_cc_callback)

        PrgChangeEvent.register_event_type_builder()
        PrgChangeEvent.register(self.program_change_callback)

        JStationSysExEvent.register_event_type_builder()

        BankDumpRequest.register()
        EndBankDumpResponse.register(self.end_bank_dump_callback)

        NotifyStore.register(self.notify_store_callback)
        NotifyUtility.register(self.notify_utility_callback)

        OneProgramRequest.register()
        OneProgramResponse.register(self.one_program_callback)

        PRGIndicesRequest.register()
        PRGIndicesResponse.register(self.program_indices_callback)

        ReceiveProgramUpdate.register(self.program_update_response)
        ReloadProgram.register()
        RequestProgramUpdate.register()

        StartBankDumpResponse.register(self.default_event_callback)

        ToMessageResponse.register(self.response_to_message_callback)

        UtilitySettingsRequest.register()
        UtilitySettingsResponse.register(self.utility_settings_callback)

        WhoAmIRequest.register(self.who_am_i_callback_req)
        WhoAmIResponse.register(self.who_am_i_callback)


        self.is_connected = False
        self.is_disconnecting = Event()
        self.is_response_received_cndt = Condition()

        self.receive_channel = -1
        self.sysex_channel = -1

        self.js_port_in = None
        self.js_port_out = None

        self.jstation_wait_for_events_thread = None


        self.main_window = main_window
        self.is_disconnecting.clear()

        self.seq = alsaseq.Sequencer('hw', app_name,
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
        self.js_port_out = midi_port_out
        self.seq.connect_ports(
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
            if self.main_window:
                self.is_response_received_cndt.acquire()
                self.send_event(UtilitySettingsRequest(self.sysex_channel))
                self.is_response_received_cndt.wait(self.RESPONSE_TIMEOUT)
                self.is_response_received_cndt.release()


    def disconnect(self):
        # sign off
        for channel in range(0, 15):
            self.send_event(CCMidiEvent(channel=channel, param=120, value=0))
            self.send_event(CCMidiEvent(channel=channel, param=64, value=0))

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
            self.send_event(BankDumpRequest(channel=self.sysex_channel))
        else:
            print('req_bank_dump: not connected')

    def req_program_update_req(self):
        if self.is_connected:
            self.send_event(RequestProgramUpdate(channel=self.sysex_channel))
        else:
            print('req_program_update_req: not connected')

    def req_program_update(self, program):
        if self.is_connected:
            self.is_response_received_cndt.acquire()
            self.send_event(ReceiveProgramUpdate(program=program,
                                                 channel=self.sysex_channel)
            )
            self.is_response_received_cndt.wait(self.RESPONSE_TIMEOUT)
            self.is_response_received_cndt.release()
        else:
            print('req_program_update: not connected')

    def req_program_change(self, program_nb):
        if self.is_connected:
            self.send_event(PrgChangeEvent(channel=self.receive_channel,
                                           value=program_nb))
        else:
            print('req_program_change: not connected')

    def reload_program(self):
        if self.is_connected:
            self.send_event(ReloadProgram(channel=self.sysex_channel))
        else:
            print('reload_program: not connected')


    def store_program(self, program):
        if self.is_connected:
            self.send_event(ReceiveProgramUpdate(channel=self.sysex_channel,
                                                 program=program))
            self.send_event(OneProgramResponse(channel=self.sysex_channel,
                                               program=program))
        else:
            print('store_program: not connected')


    def wait_for_events(self):
        event_list = list()
        while not self.is_disconnecting.is_set():
            event_list = self.seq.receive_events(self.WAIT_SHUTDOWN_TIMEOUT, 1)
            if 0 < len(event_list):
                for seq_event in event_list:
                    if None != seq_event:
#                        print('==> Received event: %s'%(seq_event))
                        event = self.factory.build_from_seq_event(seq_event)
                        if event and event.is_valid:
#                            print('\t%s'%(event))
                            event.process()
                        else:
                            if event:
                                print(event)
                            # else: seq event is dumped in the factory
                    else:
                        print('Seq event is null')
                event_list = list()
            # else: no response received (timed out)

    def default_event_callback(self, event):
        if event.is_valid:
#            print('==> received %s'%(event))
            pass
        else:
            print('Event is invalid %s'%(event))

    def who_am_i_callback_req(self, event):
#        print('Received WhoAmIRequest: am I calling myself?')
        pass

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

    def notify_store_callback(self, event):
        self.default_event_callback(event)
        one_prg_req = OneProgramRequest(channel=self.sysex_channel,
                                        bank_nb=Program.BANK_USER,
                                        prg_nb=event.prg_nb)
        self.send_event(one_prg_req)

    def notify_utility_callback(self, event):
        self.default_event_callback(event)
        settings_req = UtilitySettingsRequest(channel=self.sysex_channel)
        self.send_event(settings_req)

    def utility_settings_callback(self, event):
        self.default_event_callback(event)
        self.is_response_received_cndt.acquire()
        self.receive_channel = event.midi_channel
        self.main_window.receive_settings(event)
        self.is_response_received_cndt.notify()
        self.is_response_received_cndt.release()

    def program_indices_callback(self, event):
        self.default_event_callback(event)
        self.main_window.set_program_count(len(event.prg_indices))

    def one_program_callback(self, event):
        self.default_event_callback(event)
        self.main_window.receive_program_from_jstation(event.program)

    def end_bank_dump_callback(self, event):
        self.default_event_callback(event)
        thread = Thread(target=self.req_program_update_req, name='send req prg up')
        thread.start()

    def one_parameter_cc_callback( self, event):
        self.default_event_callback(event)
        if self.main_window != None:
            self.main_window.update_parameter_from_jstation(event.param,
                                                            event.value,
                                                            is_cc=True)
        else:
            print('Skipping: %s'%(event))

    def program_change_callback(self, event):
        self.default_event_callback(event)
        self.main_window.select_program_from_its_number(event.value)

    def program_update_response(self, event):
        self.default_event_callback(event)
        # TODO: handle 'has changed' flag also
        self.main_window.select_program_from_its_content(event.program)

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
#            print('<== sending %s'%(event))
            self.seq.output_event(event.get_seq_event())
            self.seq.drain_output()
#            print('...sent')
            success = True
        else:
            print('Failed to build seq event for: %s'%(event))
        return success

    def send_command(self, command, value):
        success = False
        return self.send_event(CCMidiEvent(self.receive_channel, command, value))
