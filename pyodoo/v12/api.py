##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2022 Fabio Castelli
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

from typing import Any, Optional, Union
from xmlrpc.client import ServerProxy

from pyodoo import BooleanOperator, Filter


class Api(object):
    """
    Odoo v12 XML-RPC API
    """
    def __init__(self,
                 model_name: str,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str = None):
        # Associate model
        if not model_name:
            raise NotImplementedError('model name was not set properly')
        self.model_name = model_name
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

        :return: The user ID for the authenticated user
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

        :param method: The name of the method to execute
        :return: Full endpoint URL
        """
        return '{ENDPOINT}/{METHOD}'.format(ENDPOINT=self.endpoint,
                                            METHOD=method)

    def get_proxy(self,
                  method: str) -> ServerProxy:
        """
        Get the proxy for the remote endpoint URL

        :param method: The name of the method to execute
        :return: A new ServerProxy object
        """
        return ServerProxy(self.build_endpoint(method=method))

    def get_proxy_object(self) -> ServerProxy:
        """
        Get the proxy for the standard object method

        :return: A new ServerProxy object for a standard Odoo objects endpoint
        """
        return ServerProxy(self.build_endpoint(method='xmlrpc/2/object'))

    @staticmethod
    def explode_filter(filters: list[Union[BooleanOperator, Filter, str]]
                       ) -> list[list[Union[str, Any]]]:
        """
        Convert a list of BooleanOperators/Filters to a list of lists

        :param filters: List of Filters or BooleanOperators
        :return: List of lists containing the exploded filter
        """
        return [[item.explode() if isinstance(item, Filter)
                 else item
                 for item in filters]]

    def do_read(self,
                entity_id: int,
                options: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Get a record in the requested model applying a filter and some
        options (like fields or context)

        :param entity_id: Object ID to get
        :param options: Dictionary with options to use
        :return: Dictionary with the requested fields
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'read',
                                   [entity_id],
                                   options)
        return results[0] if results else None

    def do_fields_get(self,
                      fields: list[str],
                      options: dict[str, Any]) -> dict[str, dict]:
        """
        Get the model fields

        :param fields: Fields list to include
        :param options: Dictionary with options to use
        :return: Dictionary with the requested fields
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'fields_get',
                                   fields,
                                   options)
        return results

    def do_search(self,
                  filters: list[Union[BooleanOperator, Filter, str]],
                  options: dict[str, Any]) -> list[int]:
        """
        Search some records in the requested model applying a filter and some
        options (like fields or context)

        :param filters: List of filters used for searching the data
        :param options: Dictionary with options to use
        :return: List of objects ID found
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'search',
                                   self.explode_filter(filters),
                                   options)
        return results

    def do_search_count(self,
                        filters: list[Union[BooleanOperator, Filter, str]],
                        options: dict[str, Any]) -> int:
        """
        Get the records count in the requested model applying a filter

        :param filters: List of filters used for searching the data
        :param options: Dictionary with options to use
        :return: Records count found
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'search_count',
                                   self.explode_filter(filters),
                                   options)
        return results

    def do_search_read(self,
                       filters: list[Union[BooleanOperator, Filter]],
                       options: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Search some records in the requested model applying a filter and some
        options (like fields or context) and returns the found data

        :param filters: List of filters used for searching the data
        :param options: Dictionary with options to use
        :return: List of dictionaries where each item is a record with the
                 requested fields
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'search_read',
                                   self.explode_filter(filters),
                                   options)
        return results

    def do_create(self,
                  values: dict[str, Any],
                  options: dict[str, Any]) -> int:
        """
        Create a new record in the requested model and returns its ID

        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        :return: The ID of the newly created object
        """
        proxy = self.get_proxy_object()
        result = proxy.execute_kw(self.database,
                                  self.uid,
                                  self.password,
                                  self.model_name,
                                  'create',
                                  [values],
                                  options)
        return result

    def do_update(self,
                  entity_id: int,
                  values: dict[str, Any],
                  options: dict[str, Any]) -> bool:
        """
        Update a record in the requested model

        :param entity_id: object ID to update
        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        :return: True if the record was updated
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'write',
                                   [[entity_id], values],
                                   options)
        return results

    def do_delete(self,
                  entity_id: int,
                  options: dict[str, Any]) -> bool:
        """
        Delete a record in the requested model

        :param entity_id: Object ID to get
        :param options: Dictionary with options to use
        :return: True if the record was updated
        """
        proxy = self.get_proxy_object()
        results = proxy.execute_kw(self.database,
                                   self.uid,
                                   self.password,
                                   self.model_name,
                                   'unlink',
                                   [entity_id],
                                   options)
        return results
