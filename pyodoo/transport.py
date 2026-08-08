##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2026 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from typing import Any
from xmlrpc.client import SafeTransport, Transport


class TimeoutHttpTransport(Transport):
    """
    XML-RPC transport with configurable timeout for HTTP endpoints.
    """
    def __init__(self,
                 timeout: float,
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def make_connection(self,
                        host: str
                        ) -> Any:
        """
        Custom make_connection method to set the socket timeout

        :param host: destination host
        :return: connection object
        """
        connection = super().make_connection(host=host)
        connection.timeout = self.timeout
        if connection.sock:
            connection.sock.settimeout(self.timeout)
        return connection


class TimeoutHttpsTransport(SafeTransport):
    """
    XML-RPC transport with configurable timeout for HTTPS endpoints.
    """
    def __init__(self,
                 timeout: float,
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def make_connection(self,
                        host: str
                        ) -> Any:
        """
        Custom make_connection method to set the socket timeout

        :param host: destination host
        :return: connection object
        """
        connection = super().make_connection(host=host)
        connection.timeout = self.timeout
        if connection.sock:
            connection.sock.settimeout(self.timeout)
        return connection
