"""
 gstation-edit Program definition
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

from gstation_edit.midi.split_bytes import SplitBytesHelpher

class Program:
    PROGRAM_BUFFER_LEN = 88

    NAME_MAX_LEN = 20 # char count

    BANK_FACTORY = 0
    BANK_USER = 1

    @classmethod
    def get_bank_name(class_, bank_nb):
        bank_name = 'undefined'
        if bank_nb >= 0:
            if bank_nb == Program.BANK_USER:
                bank_name = 'user'
            elif bank_nb == Program.BANK_FACTORY:
                bank_name = 'factory'
            else:
                bank_name = 'unknown'
        return bank_name


    def __init__(self, bank=-1, number=-1, data=None, name='',
                 data_buffer=None, has_changed=False):
        self.helper = SplitBytesHelpher()

        self.bank = bank
        self.number = number
        self.original_data = data
        self.original_name = name

        if data_buffer:
            self.original_data = list()
            index = 0
            while index < self.PROGRAM_BUFFER_LEN:
                self.original_data.append(
                    self.helper.get_value_from_split_bytes(
                        data_buffer[index : index+2]
                    )
                )
                index += 2

            self.original_name = ''
            index = self.PROGRAM_BUFFER_LEN
            while index < len(data_buffer):
                value = self.helper.get_value_from_split_bytes(
                        data_buffer[index : index+2]
                    )
                if value != 0:
                    self.original_name += chr(value)
                else:
                    break
                index += 2

        self.data = list(self.original_data)
        self.name = str(self.original_name)
        self.has_changed = has_changed


    def get_data_buffer(self, with_has_changed=False):
        data = list()

        program_changed_flag = 0
        if self.has_changed:
            program_changed_flag = 1

        if with_has_changed:
            data.append(program_changed_flag)

        data += self.data

        for index in range(0, min(len(self.name), self.NAME_MAX_LEN)):
            data.append(ord(self.name[index]))
        data.append(0) # 0 ending for name

        return data


    def change_parameter(self, parameter_nb, value):
        if self.data[parameter_nb] != value:
            self.data[parameter_nb] = value
            if self.original_data[parameter_nb] == value:
                # back to original value => check if Program is back to original state
                self.has_changed = not self.is_same_name_and_data(
                    self.original_name,
                    self.original_data
                )
            else:
                self.has_changed = True

    def restore_original(self):
        self.name = str(self.original_name)
        self.data = list(self.original_data)
        self.has_changed = False

    def apply_changes(self):
        self.original_name = str(self.name)
        self.original_data = list(self.data)
        self.has_changed = False

    def rename(self, new_name):
        if self.name != new_name:
            self.name = new_name
            if self.original_name == new_name:
                # back to original name => check if Program is back to original state
                self.has_changed = not self.is_same_name_and_data(
                    self.original_name,
                    self.original_data
                )
            else:
                self.has_changed = True

    def is_same_as(self, other_program):
        return self.is_same_name_and_data(other_program.name, other_program.data)

    def is_same_name_and_data(self, other_name, other_data):
        result = True
        if other_name == self.name:
            for index in range(0, len(self.original_data)):
                if other_data[index] != self.data[index]:
                    result = False
                    break
        else:
            result = False
        return result

    def __str__(self):
        return 'prg bank: %s, prg nb: %d, '\
                'has_changed: %d, prg name: %s, '\
                'prg data: %s'\
                %(self.get_bank_name(self.bank), self.number,
                  self.has_changed, self.name,
                  ["%02d: %02d"%(index, self.data[index]) \
                   for index in range(0, len(self.data))])

