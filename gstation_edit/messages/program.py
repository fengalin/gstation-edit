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

class Program:
    PARAM_COUNT = 44

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
                 sysex_buffer=None, data_len=-1, has_changed=False):
        self.bank = bank
        self.number = number
        self.original_data = data
        self.original_name = name

        self.data = None
        self.name = None
        self.has_changed = False

        self.is_valid = True

        if sysex_buffer and data_len > self.PARAM_COUNT:
            self.original_data = list()
            index = 0
            for index in range(0, self.PARAM_COUNT):
                value = sysex_buffer.pop_split_bytes(2)
                if value != None:
                    self.original_data.append(value)
                else:
                    self.is_valid = False
                    break

            index += 1

            if self.is_valid:
                is_complete = False
                self.original_name = ''
                while index < data_len:
                    value = sysex_buffer.pop_split_bytes(2)
                    if value != None:
                        index += 1
                        if not is_complete and value != 0:
                            if value > 0 and value < 128:
                                self.original_name += chr(value)
                            else:
                                self.is_valid = False
                                break
                        else:
                            # end of string
                            is_complete = True
                    else:
                        self.is_valid = False
                        break

        if self.is_valid:
            self.data = list(self.original_data)
            self.name = str(self.original_name)
            self.has_changed = has_changed
        else:
            print('Could not parse program from buffer: '\
                  'data len: %d, data index: %d - %s'%(
                    data_len, index,
                    sysex_buffer.get_readable_from_marker()
                )
            )


    def copy(self):
        return Program(bank=self.bank, number=self.number,
                       data=list(self.data), name=str(self.name))

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

    def change_to(self, other_program):
        if not self.is_same_as(other_program):
            self.name = other_program.name
            self.data = other_program.data
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
        prg_data = 'invalid'
        if self.is_valid:
            prg_data = 'prg data: %s'%(
                ["%02d: %02d"%(index, self.data[index]) \
                   for index in range(0, len(self.data))])
        return 'prg bank: %s, prg nb: %d, '\
                'has_changed: %d, prg name: %s, %s'\
                %(self.get_bank_name(self.bank), self.number,
                  self.has_changed, self.name, prg_data
                  )

