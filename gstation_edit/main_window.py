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

from gstation_edit.messages.one_prg_dump import OneProgramDump


class MainWindow:
    def __init__(self, app_name, gtk_builder):
        self.gtk_builder = gtk_builder
        self.gtk_window = self.gtk_builder.get_object('main-window')

        self.gtk_window.show_all()

        self.programs = dict()
        self.program_count = 0
        self.current_program = None
        self.current_selected_iter = None

        self.jstation_interface = JStationInterface(app_name, self)

        self.init_widgets()

        self.init_parameters_dictionnaries()


    def connect(self):
        # TODO: use a property file to store the midi connection ports
        self.midi_select_dlg.present()

    def on_connected(self, midi_port_in, midi_port_out):
        if self.jstation_interface.is_connected:
            self.jstation_interface.req_bank_dump()
        self.midi_select_dlg.hide()

    def quit(self):
        self.jstation_interface.disconnect()

    def init_widgets(self):
        self.parameter_bindings = dict()
        self.parameter_cc_bindings = dict()

        header_bar = self.gtk_builder.get_object('header-bar')
        self.gtk_window.set_titlebar(header_bar)

        self.init_undo_store()
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

            self.menu_item_export = Gtk.MenuItem('Export...')
            self.menu_item_export.connect('activate', self.context_menu_export)
            self.context_menu_widget.insert(self.menu_item_export, 2)
            self.menu_item_export.set_sensitive(False)

            menu_item_import = Gtk.MenuItem('Import...')
            menu_item_import.connect('activate', self.context_menu_import)
            self.context_menu_widget.insert(menu_item_import, 3)
            menu_item_import.set_sensitive(False)

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
                self.undo_btn.set_sensitive(True)
                self.menu_item_undo.set_sensitive(True)
                self.store_btn.set_sensitive(True)
                self.menu_item_store.set_sensitive(True)
            else:
                self.undo_btn.set_sensitive(False)
                self.menu_item_undo.set_sensitive(False)
                self.store_btn.set_sensitive(False)
                self.menu_item_store.set_sensitive(False)

            self.bank_list_model.set(self.current_selected_iter, 2, flag)

    def set_program_count(self, program_count):
        self.program_count = program_count
        self.bank_list_model.clear()

    def receive_program_from_jstation(self, program):
        local_program = self.programs.get(program.number)
        if local_program == None:
            loc_str = '%d.%d' %(program.number//3, program.number%3 + 1)
            self.bank_list_model.append([program.number, loc_str, '', program.name])
        self.programs[program.number] = program
        if self.current_program:
            if self.current_program.number == program.number:
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
            self.menu_item_export.set_sensitive(True)
        else:
            # TODO: factory banks can be accessed outside of the user banks
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


    def undo_changes(self):
        self.current_program.restore_original()
        self.init_parameters()
        self.set_current_name(self.current_program.name)
        self.jstation_interface.reload_program()

    def on_undo_clicked(self, widget):
        if self.current_program:
            self.undo_changes()

    def on_store_clicked(self, widget):
        if self.current_program:
            self.current_program.apply_changes()
            self.jstation_interface.store_program(self.current_program)
            self.set_program_has_changed(False)


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

    def context_menu_import(self, widget, *args):
        # TODO: implement !
        print('Import clicked %s'%(args))

    def context_menu_export(self, widget, *args):
        prg_dump = OneProgramDump(program=self.current_program, isolated=True)
        prg_dump.build_sysex_buffer()
        print('Export: %s'%(prg_dump))


    def context_menu_copy(self, widget, *args):
        # TODO: implement !
        print('Copy clicked %s'%(args))

    def context_menu_paste(self, widget, *args):
        # TODO: implement !
        print('Paste clicked %s'%(args))
