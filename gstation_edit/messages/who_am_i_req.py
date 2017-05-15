"""
 gstation-edit WhoAmIRequest definition
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

from jstation_sysex_req import *

class WhoAmIRequest(JStationSysExRequest):
    RESP_ON_CHANNEL = 0
    RESP_ON_7f = 1

    def __init__(self, channel_id=JStationSysExRequest.ALL_CHANNELS):
        JStationSysExRequest.__init__(self, channel_id=channel_id,
                                      procedure_id=0x40, version=1)
        self.response_on = self.RESP_ON_7f

    def build_data_buffer(self):
        JStationSysExRequest.build_data_buffer(self)
        if self.is_valid:
            if 0 < len(self.data_buffer):
                if self.RESP_ON_CHANNEL == self.response_on or \
                        self.RESP_ON_7f == self.response_on:
                    self.data_buffer += self.get_split_bytes_from_value(self.response_on)
                    self.is_valid = True
                else:
                    self.data_buffer = list()
                    self.is_valid = False
                    print('Response on not defined for ReqWhoAmI SysEx')

    def __str__(self):
        return "%s. Version: %d, response on %d"%(self.__class__.__name__,
                                                  self.version,
                                                  self.response_on)
