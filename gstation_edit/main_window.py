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
from gstation_edit.rack.wha_expression import WhaExpressionUnit

from gstation_edit.midi_select_dlg import MidiSelectDlg
from gstation_edit.utilities_dlg import UtilitiesDlg
from gstation_edit.jstation_interface import JStationInterface


class MainWindow:
    def __init__(self, app_name, gtk_builder):
        self._gtk_builder = gtk_builder
        self.gtk_window = self._gtk_builder.get_object('main-window')

        self.gtk_window.show_all()

        self._programs = dict()
        self._program_count = 0
        self._current_program = None
        self._current_selected_iter = None

        self._jstation_interface = JStationInterface(app_name, self)

        self.init_widgets()

        self.init_parameters_dictionnaries()


    def connect(self):
        # TODO: use a property file to store the midi connection ports
        self._midi_select_dlg.present()

    def request_bank_dump(self):
        if self._jstation_interface.is_connected:
            self._jstation_interface.req_bank_dump()

    def quit(self):
        self._jstation_interface.disconnect()

    def init_widgets(self):
        self._signal_handlers = dict()
        self._parameter_bindings = dict()
        self._parameter_cc_bindings = dict()

        header_bar = self._gtk_builder.get_object('header-bar')
        self.gtk_window.set_titlebar(header_bar)

        self.init_undo_store()
        self.init_utilities_dlg()
        self.init_rename_dlg()
        self.init_midi_select_dlg()

        self._units = list()
        self._units.append(CompressorGateUnit(self))
        self._units.append(AmpUnit(self))
        self._units.append(EffectUnit(self))
        self._units.append(DelayUnit(self))
        self._units.append(ReverbUnit(self))
        self._units.append(WhaExpressionUnit(self))

        self.init_bank_list_widget()
        self.init_context_menu_widget()
        for unit in self._units:
            unit.init_widgets(self._gtk_builder)

    def init_midi_select_dlg(self):
        midi_options_btn = self._gtk_builder.get_object('midi-options-btn')
        self._midi_select_dlg = MidiSelectDlg(self,
                                              self._jstation_interface,
                                              self._gtk_builder)
        midi_options_btn.connect('clicked',
                                 self._midi_select_dlg.present)
        self._signal_handlers.update(self._midi_select_dlg.get_signal_handlers())

    def init_utilities_dlg(self):
        utilities_btn = self._gtk_builder.get_object('utilities-btn')
        self._utilities_dlg = UtilitiesDlg(self, self._gtk_builder)
        utilities_btn.connect('clicked',
                              self._utilities_dlg.present)
        self._signal_handlers.update(self._utilities_dlg.get_signal_handlers())
        self._parameter_cc_bindings.update(
            self._utilities_dlg.get_parameter_cc_bindings()
        )

    def init_undo_store(self):
        self.undo_btn = self._gtk_builder.get_object('undo-btn')
        self.undo_btn.set_sensitive(False)
        self.undo_btn.connect('clicked', self.on_undo_clicked)

        self.store_btn = self._gtk_builder.get_object('store-btn')
        self.store_btn.set_sensitive(False)
        self.store_btn.connect('clicked', self.on_store_clicked)

    def init_bank_list_widget(self):
        self._bank_list_widget = self._gtk_builder.get_object('bank-list-trv')
        if self._bank_list_widget:
            self._bank_list_model = self._bank_list_widget.get_model()

            column_loc = Gtk.TreeViewColumn('Loc.')
            self._bank_list_widget.append_column(column_loc)
            cell_loc = Gtk.CellRendererText()
            column_loc.pack_start(cell_loc, True)
            column_loc.add_attribute(cell_loc, 'text', 1)

            column_name = Gtk.TreeViewColumn('*')
            self._bank_list_widget.append_column(column_name)
            cell_name = Gtk.CellRendererText()
            column_name.pack_start(cell_name, True)
            column_name.add_attribute(cell_name, 'text', 2)

            column_name = Gtk.TreeViewColumn('Bank Name')
            self._bank_list_widget.append_column(column_name)
            cell_name = Gtk.CellRendererText()
            column_name.pack_start(cell_name, True)
            column_name.add_attribute(cell_name, 'text', 3)
        else:
            self._bank_list_model = None
            print('Could not find widget for bank list')

    def init_context_menu_widget(self):
        self._context_menu_widget = \
                                 self._gtk_builder.get_object('context-menu')
        self._context_menu_widget.attach_to_widget(self._bank_list_widget)

        if self._context_menu_widget:
            self.menu_item_store = Gtk.MenuItem('Store changes')
            self.menu_item_store.connect('activate', self.context_menu_store)
            self._context_menu_widget.insert(self.menu_item_store, 1)
            self.menu_item_store.set_sensitive(False)

            self.menu_item_undo = Gtk.MenuItem('Undo changes')
            self.menu_item_undo.connect('activate', self.context_menu_undo)
            self._context_menu_widget.insert(self.menu_item_undo, 2)
            self.menu_item_undo.set_sensitive(False)

            menu_item_rename = Gtk.MenuItem('Rename...')
            menu_item_rename.connect( 'activate', self.context_menu_rename)
            self._context_menu_widget.insert(menu_item_rename, 0)
            menu_item_rename.set_sensitive(False)

            menu_item_export = Gtk.MenuItem('Export...')
            menu_item_export.connect('activate', self.context_menu_export)
            self._context_menu_widget.insert(menu_item_export, 3)
            menu_item_export.set_sensitive(False)

            menu_item_import = Gtk.MenuItem('Import...')
            menu_item_import.connect('activate', self.context_menu_import)
            self._context_menu_widget.insert(menu_item_import, 4)
            menu_item_import.set_sensitive(False)

            menu_item_copy = Gtk.MenuItem('Copy')
            menu_item_copy.connect('activate', self.context_menu_copy)
            self._context_menu_widget.insert(menu_item_copy, 5)
            menu_item_copy.set_sensitive(False)

            menu_item_paste = Gtk.MenuItem('Paste')
            menu_item_paste.set_sensitive(False)
            menu_item_paste.connect('activate', self.context_menu_paste)
            self._context_menu_widget.insert(menu_item_paste, 6)
            menu_item_paste.set_sensitive(False)
        else:
            print('Could not find widget for context menu')

    def init_rename_dlg(self):
        self._rename_dlg = self._gtk_builder.get_object('rename-dlg')
        self._rename_entry = self._gtk_builder.get_object('rename-entry')

    def get_signal_handlers(self):
        return self._signal_handlers

    def init_parameters_dictionnaries(self):
        self._signal_handlers['on_bank-list-trv_cursor_changed'] = \
                                                    self.select_program_from_ui
        self._signal_handlers['on_bank-list-trv_button_press_event'] = \
                                                    self.popup_context_menu

        for unit in self._units:
            self._signal_handlers.update(unit.get_signal_handlers())
            self._parameter_bindings.update(unit.get_parameter_bindings())
            self._parameter_cc_bindings.update(unit.get_parameter_cc_bindings())

    def send_parameter_value(self, parameter, program_has_changed=True):
        if program_has_changed:
            self._current_program.change_parameter(parameter.parameter_nb,
                                                   parameter.value)
            self.set_program_has_changed(self._current_program.has_changed)
        if self._jstation_interface.is_connected:
            self._jstation_interface.send_command(parameter.cc_nb,
                                                  parameter.get_cc_value())

    def set_program_has_changed(self, has_changed):
        if self._current_selected_iter:
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

            self._bank_list_model.set(self._current_selected_iter, 2, flag)

    def set_program_count(self, program_count):
        self._program_count = program_count
        self._bank_list_model.clear()

    def receive_program_from_jstation(self, program):
        local_program = self._programs.get(program.number)
        if local_program == None:
            loc_str = '%d.%d' %(program.number//3, program.number%3 + 1)
            self._bank_list_model.append([program.number, loc_str, '', program.name])
        self._programs[program.number] = program
        if self._current_program:
            if self._current_program.number == program.number:
                self.init_parameters()

    def select_program_from_its_number(self, program_nb):
        self.set_current_program(program_nb)
        self.select_program_in_list(program_nb)

    def set_current_program(self, program_nb):
        program = self._programs.get(program_nb)
        if program:
            if self._current_program:
                if self._current_program.has_changed:
                    self._current_program.restore_original()
                    self.set_current_name(self._current_program.name)
                    self.set_program_has_changed(False)
            self._current_program = program
            self.init_parameters()
        else:
            # TODO: factory banks can be accessed outside of the user banks
            print('Unknown program selection %d out of bounds'%(program))

    def select_program_in_list(self, program_nb):
        tree_iter = None
        try:
            tree_iter = self._bank_list_model.get_iter_from_string(str(program_nb))
        except ValueError:
            can_be_selected = False
        if tree_iter:
            tree_selection = self._bank_list_widget.get_selection()
            tree_selection.select_iter(tree_iter)
            self._current_selected_iter = tree_iter
        else:
            print('Cannot select program %d'%(program_nb))

    def select_program_from_its_content(self, program):
        # select a program without knowing its number, but from its name and data
        for cur_prg in self._programs.values():
            if program.is_same_as(cur_prg):
                self.select_program_from_its_number(cur_prg.number)
                break
        if self._current_program == None:
            self.select_program_from_its_number(0)

    def init_parameters(self):
        for index in range(0, len(self._current_program.data)):
            parameter = self._parameter_bindings.get(index)
            if parameter:
                parameter.init_value(self._current_program.data[index])
        self.set_program_has_changed(False)

    def update_parameter_from_jstation(self, parameter, value, is_cc):
        if is_cc:
            parameter = self._parameter_cc_bindings.get(parameter)
            if parameter:
                parameter.init_value(value=value, is_cc=True)
                if parameter.parameter_nb != -1:
                    self._current_program.change_parameter(parameter.parameter_nb,
                                                           parameter.value)
                    self.set_program_has_changed(self._current_program.has_changed)
        else:
            print('Updating isolated parameters other than with CC command not implemented')

    def select_program_from_ui(self, widget):
        # TODO: find out what this is supposed to do since J-Station does not store update
        if self._current_program.has_changed:
            self._jstation_interface.req_program_update(self._current_program)
            # TODO: something else should be done here (update ui, ??)

        tree_iter = self._bank_list_widget.get_selection().get_selected()[1]
        selected_program_nb = int(self._bank_list_model.get_value(tree_iter, 0))
        self.set_current_program(selected_program_nb)
        self._current_selected_iter = \
                        self._bank_list_widget.get_selection().get_selected()[1]
        self._jstation_interface.req_program_change(selected_program_nb)


    def on_undo_clicked(self, widget):
        if self._current_program:
            self._current_program.restore_original()
            self.init_parameters()
            self._jstation_interface.reload_program()

    def on_store_clicked(self, widget):
        if self._current_program:
            self._current_program.apply_changes()
            self._jstation_interface.store_program(self._current_program)
            self.set_program_has_changed(False)


    def receive_settings(self, settings):
        self._utilities_dlg.set_utilities(settings)

    def send_settings(self, settings):
        self._jstation_interface.send_event(settings)

    def popup_context_menu(self, widget, event):
        if event.button == 3:
            # right click
            self._context_menu_widget.popup(None, None, None, None,
                                            event.button, event.time)
            self._context_menu_widget.show_all()
            return True

    def set_current_name(self, name):
        self._bank_list_model.set(self._current_selected_iter, 3, name)

    def context_menu_rename(self, widget, *arg):
        if self._current_program:
            original_name = self._current_program.name
            self._rename_entry.set_text(original_name)
            result = self._rename_dlg.run()
            if Gtk.RESPONSE_APPLY == result:
                new_name = self._rename_entry.get_text()
                if original_name != new_name:
                    # TODO: should check names max length
                    self._current_program.rename(new_name)
                    self.set_program_has_changed(self._current_program.has_changed)
                    self.set_current_name(new_name)
            self.rename_dlg.hide()

    def context_menu_store(self, widget, *arg):
        self.on_store_clicked(widget)

    def context_menu_undo(self, widget, *arg):
        self.on_undo_clicked(widget)

    def context_menu_import(self, widget, *arg):
        # TODO: implement !
        print('Import clicked %s'%(arg))

    def context_menu_export(self, widget, *arg):
        # TODO: implement !
        print('Export clicked %s'%(arg))

    def context_menu_copy(self, widget, *arg):
        # TODO: implement !
        print('Copy clicked %s'%(arg))

    def context_menu_paste(self, widget, *arg):
        # TODO: implement !
        print('Paste clicked %s'%(arg))

