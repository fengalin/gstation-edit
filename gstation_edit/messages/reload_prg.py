"""
 gstation-edit ReloadProgram definition
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

from gstation_edit.messages.jstation_sysex_event import JStationSysexEvent

class ReloadProgram(JStationSysexEvent):
    PROCEDURE_ID = 0x20
    VERSION = 1

    def __init__(self, channel=-1, sysex_buffer=None):
        JStationSysexEvent.__init__(self, channel, sysex_buffer)

    # Build to send defined in JStationSysexEvent

