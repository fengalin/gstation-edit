"""
 gstation-edit MainWindow definition
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
# with this program.    If not, see <http://www.gnu.org/licenses/>.


from os import path
from os import makedirs

import struct

from ConfigParser import SafeConfigParser

from gi.repository import Gtk

from gstation_edit.rack.amp import AmpUnit
from gstation_edit.rack.compress_gate import CompressorGateUnit
from gstation_edit.rack.effect import EffectUnit
from gstation_edit.rack.delay import DelayUnit
from gstation_edit.rack.reverb import ReverbUnit
from gstation_edit.rack.wah_expression import WahExpressionUnit

from gstation_edit.midi_select_dlg import MidiSelectDlg
from gstation_edit.utilities_dlg import UtilitiesDlg
from gstation_edit.jstation_interface import JStationInterface

from gstation_edit.midi.sysex_buffer import SysexBuffer

from gstation_edit.messages.jstation_sysex_event import JStationSysexEvent
from gstation_edit.messages.bank_dump import BankDump
from gstation_edit.messages.one_prg_dump import OneProgramDump


class MainWindow:
    def __init__(self, app_name, gtk_builder):

        self.config = SafeConfigParser(allow_no_value=True)
        config_base_path = path.expanduser('~/.config/gstation-edit')
        if not path.isdir(config_base_path):
            makedirs(config_base_path)
        self.config_path = path.join(config_base_path, 'settings.cfg')
        self.config.read(self.config_path)

        self.gtk_builder = gtk_builder
        self.gtk_window = self.gtk_builder.get_object('main-window')

        self.gtk_window.show_all()

        self.programs = dict()
        self.program_count = 0
        self.current_program = None
        self.current_selected_iter = None

        self.jstation_interface = JStationInterface(app_name, self)
        BankDump.register()
        OneProgramDump.register()

        self.init_widgets()

        self.init_parameters_dictionnaries()


    def connect(self):
        midi_port_in = None
        midi_port_out = None
        if self.config.has_section('MIDI'):
            midi_port_in = self.config.get('MIDI', 'port_in')
            midi_port_out = self.config.get('MIDI', 'port_out')

        if midi_port_in and midi_port_out:
            self.jstation_interface.connect(midi_port_in, midi_port_out, 1)
            if self.jstation_interface.is_connected:
                self.midi_select_dlg.set_defaults(midi_port_in, midi_port_out)
                self.midi_select_dlg.set_connected()
                self.on_connected(midi_port_in, midi_port_out)
            else:
                # could not connect using settings
                self.midi_select_dlg.post_connection_actions()
                self.midi_select_dlg.present()
        else:
            self.midi_select_dlg.present()

    def on_connected(self, midi_port_in, midi_port_out):
        if self.jstation_interface.is_connected:
            if not self.config.has_section('MIDI'):
                self.config.add_section('MIDI')
            self.config.set('MIDI', 'port_in', midi_port_in)
            self.config.set('MIDI', 'port_out', midi_port_out)

            self.clear()

            self.jstation_interface.req_bank_dump()
        self.midi_select_dlg.hide()

    def quit(self):
        with open(self.config_path, 'wb') as configfile:
            self.config.write(configfile)

        self.jstation_interface.disconnect()

    def init_widgets(self):
        self.parameter_bindings = dict()
        self.parameter_cc_bindings = dict()

        header_bar = self.gtk_builder.get_object('header-bar')
        self.gtk_window.set_titlebar(header_bar)

        self.init_undo_store()
        self.init_bank_buttons()
        self.init_utilities_dlg()
        self.init_midi_select_dlg()

        self.units = list()
        self.units.append(CompressorGateUnit(self))
        self.units.append(AmpUnit(self))
        self.units.append(EffectUnit(self))
        self.units.append(DelayUnit(self))
        self.units.append(ReverbUnit(self))
        self.units.append(WahExpressionUnit(self))

        self.init_bank_list_widget()
        self.init_context_menu_widget()

        for unit in self.units:
            unit.init_widgets(self.gtk_builder)

    def init_midi_select_dlg(self):
        midi_options_btn = self.gtk_builder.get_object('midi-options-btn')
        self.midi_select_dlg = MidiSelectDlg(self.gtk_builder, self,
                                             self.jstation_interface,
                                             self.on_connected)
        midi_options_btn.connect('clicked', self.midi_select_dlg.present)

    def init_utilities_dlg(self):
        utilities_btn = self.gtk_builder.get_object('utilities-btn')
        self.utilities_dlg = UtilitiesDlg(self, self.gtk_builder)
        utilities_btn.connect('clicked',
                              self.utilities_dlg.present)
        self.parameter_cc_bindings.update(
            self.utilities_dlg.get_parameter_cc_bindings()
        )

    def init_undo_store(self):
        self.undo_btn = self.gtk_builder.get_object('undo-btn')
        self.undo_btn.set_sensitive(False)
        self.undo_btn.connect('clicked', self.on_undo_clicked)

        self.store_btn = self.gtk_builder.get_object('store-btn')
        self.store_btn.set_sensitive(False)
        self.store_btn.connect('clicked', self.on_store_clicked)

    def init_bank_buttons(self):
        self.export_bank_btn = self.gtk_builder.get_object('export-bank-btn')
        self.export_bank_btn.set_sensitive(False)
        self.export_bank_btn.connect('clicked', self.on_export_bank_clicked)

        self.import_bank_btn = self.gtk_builder.get_object('import-bank-btn')
        self.import_bank_btn.set_sensitive(False)
        self.import_bank_btn.connect('clicked', self.import_prg_or_bank)

    def init_bank_list_widget(self):
        self.bank_list_widget = self.gtk_builder.get_object('bank-list-trv')
        if self.bank_list_widget:
            self.bank_list_model = Gtk.ListStore(int, str, str, str)
            self.bank_list_widget.set_model(self.bank_list_model)

            # Note: column 0 contains program number but is not rendered

            column_loc = Gtk.TreeViewColumn('Loc.',
                                            Gtk.CellRendererText(),
                                            text=1)
            self.bank_list_widget.append_column(column_loc)

            column_changed = Gtk.TreeViewColumn('*',
                                                Gtk.CellRendererText(),
                                                text=2)
            self.bank_list_widget.append_column(column_changed)

            cell_name = Gtk.CellRendererText()
            cell_name.set_property('editable', True)
            column_name = Gtk.TreeViewColumn('Bank Name', cell_name, text=3)
            self.bank_list_widget.append_column(column_name)
            cell_name.connect('edited', self.on_prog_name_edited)

            self.bank_list_widget.connect('cursor_changed',
                                          self.select_program_from_ui)
            self.bank_list_widget.connect('button_press_event',
                                          self.popup_context_menu)
        else:
            self.bank_list_model = None
            print('Could not find widget for bank list')


    def clear(self):
        self.bank_list_model.clear()
        self.programs = dict()
        self.program_count = 0
        self.current_program = None
        self.current_selected_iter = None


    def init_context_menu_widget(self):
        self.context_menu_widget = self.gtk_builder.get_object('context-menu')
        self.context_menu_widget.attach_to_widget(self.bank_list_widget)

        if self.context_menu_widget:
            self.menu_item_store = Gtk.MenuItem('Store changes')
            self.menu_item_store.connect('activate', self.context_menu_store)
            self.context_menu_widget.insert(self.menu_item_store, 0)
            self.menu_item_store.set_sensitive(False)

            self.menu_item_undo = Gtk.MenuItem('Undo changes')
            self.menu_item_undo.connect('activate', self.context_menu_undo)
            self.context_menu_widget.insert(self.menu_item_undo, 1)
            self.menu_item_undo.set_sensitive(False)

            self.menu_item_export = Gtk.MenuItem('Export program...')
            self.menu_item_export.connect('activate',
                                          self.context_menu_export_prg)
            self.context_menu_widget.insert(self.menu_item_export, 2)
            self.menu_item_export.set_sensitive(False)

            self.menu_item_import = Gtk.MenuItem('Import...')
            self.menu_item_import.connect('activate', self.import_prg_or_bank)
            self.context_menu_widget.insert(self.menu_item_import, 3)
            self.menu_item_import.set_sensitive(False)

            menu_item_copy = Gtk.MenuItem('Copy')
            menu_item_copy.connect('activate', self.context_menu_copy)
            self.context_menu_widget.insert(menu_item_copy, 4)
            menu_item_copy.set_sensitive(False)

            menu_item_paste = Gtk.MenuItem('Paste')
            menu_item_paste.set_sensitive(False)
            menu_item_paste.connect('activate', self.context_menu_paste)
            self.context_menu_widget.insert(menu_item_paste, 5)
            menu_item_paste.set_sensitive(False)
        else:
            print('Could not find widget for context menu')


    def init_parameters_dictionnaries(self):
        for unit in self.units:
            self.parameter_bindings.update(unit.get_parameter_bindings())
            self.parameter_cc_bindings.update(unit.get_parameter_cc_bindings())

    def send_parameter_value(self, parameter, program_has_changed=True):
        if program_has_changed:
            self.current_program.change_parameter(parameter.parameter_nb,
                                                  parameter.value)
            self.set_program_has_changed(self.current_program.has_changed)
        if self.jstation_interface.is_connected:
            self.jstation_interface.send_command(parameter.cc_nb,
                                                 parameter.get_cc_value())

    def set_program_has_changed(self, has_changed):
        if self.current_selected_iter:
            flag = ''
            if has_changed:
                flag = '*'
            self.bank_list_model.set(self.current_selected_iter, 2, flag)
            self.set_has_changes(has_changed)

    def set_has_changes(self, has_changes):
        if has_changes:
            self.undo_btn.set_sensitive(True)
            self.menu_item_undo.set_sensitive(True)
            self.store_btn.set_sensitive(True)
            self.menu_item_store.set_sensitive(True)
        else:
            self.undo_btn.set_sensitive(False)
            self.menu_item_undo.set_sensitive(False)
            self.store_btn.set_sensitive(False)
            self.menu_item_store.set_sensitive(False)


    def set_program_count(self, program_count):
        self.program_count = program_count
        self.bank_list_model.clear()

    def receive_program(self, program):
        local_program = self.programs.get(program.number)
        if local_program == None:
            loc_str = '%d.%d' %(program.number//3, program.number%3 + 1)
            self.bank_list_model.append([program.number, loc_str, '', program.name])
        self.programs[program.number] = program
        if self.current_program and self.current_program.number == program.number:
            self.current_program = program
            self.init_parameters()

    def select_program_from_its_number(self, program_nb):
        self.set_current_program(program_nb)
        self.select_program_in_list(program_nb)

    def set_current_program(self, program_nb):
        program = self.programs.get(program_nb)
        if program:
            if self.current_program:
                if self.current_program.has_changed:
                    self.current_program.restore_original()
                    self.set_current_name(self.current_program.name)
                    self.set_program_has_changed(False)
            self.current_program = program
            self.init_parameters()
            self.export_bank_btn.set_sensitive(True)
            self.import_bank_btn.set_sensitive(True)
            self.menu_item_export.set_sensitive(True)
            self.menu_item_import.set_sensitive(True)
        else:
            print('Unknown program selection %d out of bounds'%(program))

    def select_program_in_list(self, program_nb):
        tree_iter = None
        try:
            tree_iter = self.bank_list_model.get_iter_from_string(str(program_nb))
        except ValueError:
            can_be_selected = False
        if tree_iter:
            tree_selection = self.bank_list_widget.get_selection()
            tree_selection.select_iter(tree_iter)
            self.current_selected_iter = tree_iter
        else:
            print('Cannot select program %d'%(program_nb))

    def select_program_from_its_content(self, program):
        # select a program without knowing its number, but from its name and data
        for cur_prg in self.programs.values():
            if program.is_same_as(cur_prg):
                self.select_program_from_its_number(cur_prg.number)
                break
        if self.current_program == None:
            self.select_program_from_its_number(0)

    def init_parameters(self):
        for index in range(0, len(self.current_program.data)):
            parameter = self.parameter_bindings.get(index)
            if parameter:
                parameter.init_value(self.current_program.data[index])
        self.set_program_has_changed(False)

    def update_parameter_from_jstation(self, parameter, value, is_cc):
        if is_cc:
            parameter = self.parameter_cc_bindings.get(parameter)
            if parameter:
                parameter.init_value(value=value, is_cc=True)
                if parameter.parameter_nb != -1:
                    self.current_program.change_parameter(parameter.parameter_nb,
                                                          parameter.value)
                    self.set_program_has_changed(self.current_program.has_changed)
        else:
            print('Updating isolated parameters other than with CC command not implemented')

    def select_program_from_ui(self, widget):
        if self.current_selected_iter != None:
            tree_iter = self.bank_list_widget.get_selection().get_selected()[1]
            selected_program_nb = int(self.bank_list_model.get_value(tree_iter, 0))
            cur_program_nb = int(self.bank_list_model.get_value(
                    self.current_selected_iter, 0)
                )
            if selected_program_nb != cur_program_nb:
                if self.current_program.has_changed:
                    self.undo_changes()

                self.set_current_program(selected_program_nb)
                self.current_selected_iter = \
                    self.bank_list_widget.get_selection().get_selected()[1]
                self.jstation_interface.req_program_change(selected_program_nb)
            # else: program hasn't changed

    def update_program_in_list(self, program):
        tree_iter = self.bank_list_model.get_iter_from_string(
            str(program.number))
        flag = ''
        if program.has_changed:
            flag = '*'
        self.bank_list_model.set(tree_iter, 2, flag)
        self.bank_list_model.set(tree_iter, 3, program.name)

    def undo_changes(self):
        for prg_nb in self.programs:
            prg = self.programs[prg_nb]
            if prg.has_changed:
                prg.restore_original()
                if prg_nb == self.current_program.number:
                    self.init_parameters()
                    self.jstation_interface.reload_program()
                self.update_program_in_list(prg)
        self.set_has_changes(False)

    def on_undo_clicked(self, widget):
        if self.current_program:
            self.undo_changes()

    def on_store_clicked(self, widget):
        for prg_nb in self.programs:
            prg = self.programs[prg_nb]
            if prg.has_changed:
                prg.apply_changes()
                is_current = False
                if prg_nb == self.current_program.number:
                    is_current = True
                self.jstation_interface.store_program(prg, is_current=is_current)
                self.update_program_in_list(prg)
        self.set_has_changes(False)


    def receive_settings(self, settings):
        self.utilities_dlg.set_utilities(settings)

    def send_settings(self, settings):
        self.jstation_interface.send_event(settings)

    def popup_context_menu(self, widget, event):
        if event.button == 3:
            # right click
            self.context_menu_widget.popup(None, None, None, None,
                                           event.button, event.time)
            self.context_menu_widget.show_all()
            return True

    def set_current_name(self, name):
        self.bank_list_model.set(self.current_selected_iter, 3, name)

    def on_prog_name_edited(self, widget, path, new_name):
        if self.current_program:
            original_name = self.current_program.name
            if original_name != new_name:
                self.current_program.rename(new_name)
                self.set_program_has_changed(self.current_program.has_changed)
                self.set_current_name(new_name)

    def context_menu_store(self, widget, *args):
        self.on_store_clicked(widget)

    def context_menu_undo(self, widget, *args):
        self.on_undo_clicked(widget)


    def run_file_chooser(self, action, proposed_name=None):
        folder = None
        if self.config.has_section('Import-Export'):
            folder = self.config.get('Import-Export', 'folder')

        title = 'Import'
        stock_ok = Gtk.STOCK_OPEN
        if action == Gtk.FileChooserAction.SAVE:
            stock_ok = Gtk.STOCK_SAVE
            title = 'Export'

        file_chooser = Gtk.FileChooserDialog(
                title, self.gtk_window, action,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 stock_ok, Gtk.ResponseType.OK)
            )
        filter_sysex = Gtk.FileFilter()
        filter_sysex.set_name('Sysex files (.syx)')
        filter_sysex.add_pattern('*.syx')
        file_chooser.add_filter(filter_sysex)

        if Gtk.FileChooserAction.SAVE:
            file_chooser.set_do_overwrite_confirmation(True)

        if folder:
            file_chooser.set_current_folder(folder)
        if proposed_name:
            file_chooser.set_current_name('%s.syx'%(proposed_name))

        result = file_chooser.run()
        if result == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            if not self.config.has_section('Import-Export'):
                self.config.add_section('Import-Export')
            self.config.set('Import-Export', 'folder', path.dirname(filename))

        return (result, file_chooser)


    def import_prg_or_bank(self, widget, *args):
        result, file_chooser = self.run_file_chooser(Gtk.FileChooserAction.OPEN)
        if result == Gtk.ResponseType.OK:
            content = None
            # TODO: catch exception and notify the user
            with open(file_chooser.get_filename(), 'rb') as sysex_file:
                content = sysex_file.read()
            if content:
                sysex_data = list()
                byte_content = struct.unpack('B'*len(content), content)
                for value in byte_content:
                    sysex_data.append(value)
                self.import_buffer(sysex_data)
        # else: canceled
        file_chooser.destroy()

    def import_buffer(self, sysex_data):
        sysex_event = JStationSysexEvent.build_from_sysex_buffer(
            sysex_buffer=SysexBuffer(sysex_data))
        if sysex_event and sysex_event.is_valid():
            has_changes = False
            if type(sysex_event) is OneProgramDump:
                self.import_current_prg(sysex_event.program)
                has_changes |= self.current_program.has_changed

            elif type(sysex_event) is BankDump:
                for program in sysex_event.programs:
                    if program.number == self.current_program.number:
                        self.import_current_prg(program)
                        has_changes |= self.current_program.has_changed
                    else:
                        self.programs[program.number].change_to(program)
                        if self.programs[program.number].has_changed:
                            self.update_program_in_list(
                                self.programs[program.number])
                            has_changes = True
            else:
                print('Attempting to import %s'%(sysex_event))

            self.set_has_changes(has_changes)
        else:
            # TODO: feedback to user - use notification?
            print('Couldn\'t import program from buffer')

    def import_current_prg(self, new_prg):
        if self.current_program:
            self.current_program.change_to(new_prg)
            if self.current_program.has_changed:
                self.init_parameters()
                self.update_program_in_list(self.current_program)
                self.jstation_interface.send_program_update(
                    self.current_program)


    def on_export_bank_clicked(self, widget):
        default_name = 'J-Station User Bank Backup'
        result, file_chooser = self.run_file_chooser(Gtk.FileChooserAction.SAVE,
                                                     default_name)
        if result == Gtk.ResponseType.OK:
            bank_dump = BankDump(programs=self.programs.values())
            if bank_dump.is_valid():
                # TODO: catch exception and notify the user
                with open(file_chooser.get_filename(), 'wb') as sysex_file:
                    for value in bank_dump.sysex_buffer.sysex_data:
                        sysex_file.write(struct.pack('B', value))
            else:
                # TODO: feedback to user - use notification?
                print('Couldn\'t export bank')

        # else: canceled
        file_chooser.destroy()

    def context_menu_export_prg(self, widget, *args):
        result, file_chooser = self.run_file_chooser(Gtk.FileChooserAction.SAVE,
                                                     self.current_program.name)
        if result == Gtk.ResponseType.OK:
            prg_dump = OneProgramDump(
                    program=self.current_program, isolated=True
                )
            if prg_dump.is_valid():
                # TODO: catch exception and notify the user
                with open(file_chooser.get_filename(), 'wb') as sysex_file:
                    for value in prg_dump.sysex_buffer.sysex_data:
                        sysex_file.write(struct.pack('B', value))
            else:
                # TODO: feedback to user - use notification?
                print('Couldn\'t export program')

        # else: canceled
        file_chooser.destroy()


    def context_menu_copy(self, widget, *args):
        # TODO: implement !
        print('Copy clicked %s'%(args))

    def context_menu_paste(self, widget, *args):
        # TODO: implement !
        print('Paste clicked %s'%(args))
