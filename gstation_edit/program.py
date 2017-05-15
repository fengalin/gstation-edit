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
    def __init__(self, bank, number, data, name):
        self.bank = bank
        self.number = number
        self.original_data = data
        self.data = list(data)
        self.original_name = name
        self.name = str(name)
        self.has_changed = False

    def change_parameter(self, parameter_nb, value):
        if self.data[parameter_nb] != value:
            self.data[parameter_nb] = value
            if self.original_data[parameter_nb] == value:
                # back to original value => check if Program is back to original state
                self.has_changed = not self.is_the_same_name_and_data(
                    self.original_name,
                    self.original_data
                )
            else:
                self.has_changed = True

    def restore_original(self):
        self.name = str(self.original_name)
        self.data = list(self.original_data)
        self.has_changed = False

    def rename(self, new_name):
        if self.name != new_name:
            self.name = new_name
            if self.original_name == new_name:
                # back to original name => check if Program is back to original state
                self.has_changed = not self.is_the_same_name_and_data(
                    self.original_name,
                    self.original_data
                )
            else:
                self.has_changed = True

    def is_the_same_as(self, other_program):
        return self.is_the_same_name_and_data(other_program.name, other_program.data)

    def is_the_same_name_and_data(self, other_name, other_data):
        result = True
        if other_name == self.name:
            for index in range(0, len(self.original_data)):
                if other_data[index] != self.data[index]:
                    result = False
                    break
        else:
            result = False
        return result

    def __str__( self ):
        return "Prg bank: %d, prg nb: %d, prg name: %s, prg data: %s"\
                %(self.bank, self.number, self.name, str(self.data))

