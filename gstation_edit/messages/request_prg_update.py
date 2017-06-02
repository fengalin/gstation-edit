"""
 gstation-edit RequestProgramUpdateRequest definition
"""
# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009 <fengalin@free.fr>
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

from .jstation_sysex_event import JStationSysExEvent

class RequestProgramUpdate(JStationSysExEvent):
    PROCEDURE_ID = 0x60
    VERSION = 2

    def __init__(self, channel=-1, seq_event=None):
        JStationSysExEvent.__init__(self, channel, seq_event)

    # Build to send defined in JStationSysExEvent
