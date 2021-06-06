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

from typing import Any, Optional, Union
from xmlrpc.client import ServerProxy

from pyodoo import (ActiveStatusChoice,
                    BooleanOperator,
                    CompareType,
                    Filter)


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

    def set_options_language(self,
                             options: dict) -> Optional[str]:
        """
        Apply the default language context to the options

        :param options: Dictionary with any existing options
        :return: The current default language code
        """
        # Set language for translated fields
        if self.language:
            if 'context' in options:
                options['context']['lang'] = self.language
            else:
                options['context'] = {'lang': self.language}
        return self.language

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

    def get(self,
            entity_id: int,
            fields: tuple[str, ...] = None) -> Optional[dict[str, Any]]:
        """
        Get a row from a model using its ID

        :param entity_id: Object ID to query
        :param fields: Tuple with the fields to include in the response
        :return: Dictionary with the requested fields
        """
        options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.do_read(entity_id=entity_id,
                               options=options)
        return results

    def find(self,
             entity_ids: list[int],
             fields: tuple[str, ...] = None,
             is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET
             ) -> list[dict[str, Any]]:
        """
        Find some rows from a model using their ID

        :param entity_ids: Objects ID to query
        :param fields: Tuple with the fields to include in the response
        :param is_active: Additional filter for active field
        :return: List of dictionaries with the requested fields
        """
        # Add filtered IDs
        filters = [['id', CompareType.IN, entity_ids]]
        # Check for active records (Only active, only inactive or both)
        if is_active == ActiveStatusChoice.BOTH:
            filters.append(['active', CompareType.IN, is_active])
        elif is_active != ActiveStatusChoice.NOT_SET:
            filters.append(['active', CompareType.EQUAL, is_active])
        options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.do_search_read(filters=filters,
                                      options=options)
        return results

    def filter(self,
               filters: list[Union[BooleanOperator, Filter]],
               fields: tuple[str, ...] = None) -> list[dict[str, Any]]:
        """
        Find some rows from a model using some filters

        :param filters: List of filters used for searching the data
        :param fields: Tuple with the fields to include in the response
        :return: List of dictionaries with the requested fields
        """
        options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.do_search_read(filters=filters,
                                      options=options)
        return results

    def search(self,
               filters: list[Union[BooleanOperator, Filter]]) -> list[int]:
        """
        Find rows list from a list of filters

        :param filters: List of filters used for searching the data
        :return: List of ID for the objects found
        """
        options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.do_search(filters=filters,
                                 options=options)
        return results

    def create(self,
               values: dict[str, Any]) -> int:
        """
        Create a new record in the requested model and returns its ID

        :param values: Dictionary with the fields to update and their values
        :return: The ID of the newly created object
        """
        options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Create data and get results
        results = self.do_create(values=values,
                                 options=options)
        return results

    def update(self,
               entity_id: int,
               values: dict[str, Any]) -> None:
        """
        Get a row from a model using its ID

        :param entity_id: The object ID to update
        :param values: Dictionary with the fields to update and their values
        """
        options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Update data and get results
        self.do_update(entity_id=entity_id,
                       values=values,
                       options=options)

    def delete(self,
               entity_id: int) -> None:
        """
        Delete a row from a model using its ID

        :param entity_id: The object ID to delete
        """
        # Request data and get results
        self.do_delete(entity_id=entity_id)

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
                  options: dict[str, Any]) -> None:
        """
        Update a record in the requested model

        :param entity_id: object ID to update
        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        """
        proxy = self.get_proxy_object()
        proxy.execute_kw(self.database,
                         self.uid,
                         self.password,
                         self.model_name,
                         'write',
                         [[entity_id], values],
                         options)

    def do_delete(self,
                  entity_id: int) -> None:
        """
        Delete a record in the requested model

        :param entity_id: Object ID to get
        """
        proxy = self.get_proxy_object()
        proxy.execute_kw(self.database,
                         self.uid,
                         self.password,
                         self.model_name,
                         'unlink',
                         [entity_id])
