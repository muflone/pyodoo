##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
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

from xmlrpc.client import ServerProxy


class Api(object):
    """
    Odoo v12 XML-RPC API
    """
    def __init__(self,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str = None):
        self.endpoint = endpoint
        self.database = database
        self.username = username
        self.password = password
        self.language = language
        self.uid = None
        # Remove trailing / from endpoint
        if self.endpoint.endswith('/'):
            self.endpoint = self.endpoint[:-1]

    def authenticate(self) -> int:
        """
        Authenticate the session using database, username and password
        :return: user id for the authenticated user
        """
        proxy = self.get_proxy(method='xmlrpc/2/common')
        self.uid = proxy.authenticate(self.database,
                                      self.username,
                                      self.password,
                                      {})
        return self.uid

    def build_endpoint(self,
                       method: str) -> str:
        """
        Build the remote endpoint URL
        :param method: method to execute
        :return: full endpoint URL
        """
        return '{ENDPOINT}/{METHOD}'.format(ENDPOINT=self.endpoint,
                                            METHOD=method)

    def get_proxy(self,
                  method: str) -> ServerProxy:
        """
        Get the proxy for the remote endpoint URL
        :param method: method to execute
        :return: Proxy object
        """
        return ServerProxy(self.build_endpoint(method=method))

    def get_proxy_object(self) -> ServerProxy:
        """
        Get the proxy for the standard object method
        :return: Proxy object
        """
        return ServerProxy(self.build_endpoint(method='xmlrpc/2/object'))

    def set_options_language(self,
                             options: dict) -> str:
        """
        Apply the default language context to the options
        :param options: dictionary with any existing options
        :return: the default language code used
        """
        # Set language for translated fields
        if self.language:
            if 'context' in options:
                options['context']['lang'] = self.language
            else:
                options['context'] = {'lang': self.language}
        return self.language

    def search_read(self,
                    model: str,
                    filter: list[list],
                    options: dict[str]):
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   model,
                                   'search_read',
                                   filter,
                                   options)
        return results
