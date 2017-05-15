"""
 gstation-edit WhoAmIRequest test
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

from messages.who_am_i_req import *

def test():
    sysex_event = WhoAmIRequest()
    sysex_event.fill_seq_event()
    is_valid = sysex_event.is_valid
    print('event is valid ?: %d'%(is_valid))
    if is_valid:
        print(sysex_event.get_seq_event().get_data())
        print(sysex_event.data_buffer)
