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

from pyodoo import (ActiveStatusChoice,
                    BooleanOperator,
                    CompareType,
                    Filter)
from pyodoo.v12.api import Api


class Model(object):
    """
    Generic data model to interact with Odoo data models.
    """
    def __init__(self,
                 model_name: str,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str = None):
        # API object
        self.api = Api(model_name=model_name,
                       endpoint=endpoint,
                       database=database,
                       username=username,
                       password=password,
                       language=language)

    def authenticate(self) -> int:
        """
        Authenticate the session using database, username and password.

        :return: The user ID for the authenticated user
        """
        return self.api.authenticate()

    def get(self,
            entity_id: int,
            fields: tuple[str, ...] = None,
            options: dict[str, Any] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None) -> Optional[dict[str, Any]]:
        """
        Get a row from a model using its ID

        :param entity_id: Object ID to query
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: Dictionary with the requested fields
        """
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Set pagination
        self.set_pagination(options=options,
                            limit=limit,
                            offset=offset)
        # Request data and get results
        results = self.api.do_read(entity_id=entity_id,
                                   options=options)
        return results

    def all(self,
            fields: tuple[str, ...] = None,
            options: dict[str, Any] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None) -> list[dict[str, Any]]:
        """
        Get all the objects

        :param fields: Fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: List of dictionaries with the requested fields
        """
        return self.filter(filters=[],
                           fields=fields,
                           options=options,
                           limit=limit,
                           offset=offset)

    def find(self,
             entity_ids: list[int],
             fields: tuple[str, ...] = None,
             is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
             options: dict[str, Any] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> list[dict[str, Any]]:
        """
        Find some rows from a model using their ID

        :param entity_ids: Objects ID to query
        :param fields: Tuple with the fields to include in the response
        :param is_active: Additional filter for active field
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: List of dictionaries with the requested fields
        """
        # Add filtered IDs
        filters = [['id', CompareType.IN, entity_ids]]
        # Check for active records (Only active, only inactive or both)
        if is_active == ActiveStatusChoice.BOTH:
            filters.append(['active', CompareType.IN, is_active])
        elif is_active != ActiveStatusChoice.NOT_SET:
            filters.append(['active', CompareType.EQUAL, is_active])
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Set pagination
        self.set_pagination(options=options,
                            limit=limit,
                            offset=offset)
        # Request data and get results
        results = self.api.do_search_read(filters=filters,
                                          options=options)
        return results

    def filter(self,
               filters: list[Union[BooleanOperator, Filter]],
               fields: tuple[str, ...] = None,
               options: dict[str, Any] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None) -> list[dict[str, Any]]:
        """
        Find some rows from a model using some filters

        :param filters: List of filters used for searching the data
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: List of dictionaries with the requested fields
        """
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Set pagination
        self.set_pagination(options=options,
                            limit=limit,
                            offset=offset)
        # Request data and get results
        results = self.api.do_search_read(filters=filters,
                                          options=options)
        return results

    def count(self,
              filters: list[Union[BooleanOperator, Filter]],
              options: dict[str, Any] = None) -> int:
        """
        Get the rows count from a model using some filters

        :param filters: List of filters used for searching the data
        :param options: Dictionary with options to use
        :return: Rows count
        """
        if options is None:
            options = {}
        # Request data and get results
        results = self.api.do_search_count(filters=filters,
                                           options=options)
        return results

    def search(self,
               filters: list[Union[BooleanOperator, Filter]],
               options: dict[str, Any] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None) -> list[int]:
        """
        Find rows list from a list of filters

        :param filters: List of filters used for searching the data
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: List of ID for the objects found
        """
        if options is None:
            options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Set pagination
        self.set_pagination(options=options,
                            limit=limit,
                            offset=offset)
        # Request data and get results
        results = self.api.do_search(filters=filters,
                                     options=options)
        return results

    def create(self,
               values: dict[str, Any],
               options: dict[str, Any] = None) -> int:
        """
        Create a new record in the requested model and returns its ID

        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        :return: The ID of the newly created object
        """
        if options is None:
            options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Create data and get results
        results = self.api.do_create(values=values,
                                     options=options)
        return results

    def update(self,
               entity_id: int,
               values: dict[str, Any],
               options: dict[str, Any] = None) -> None:
        """
        Get a row from a model using its ID

        :param entity_id: The object ID to update
        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        """
        if options is None:
            options = {}
        # Set language for translated fields
        self.set_options_language(options=options)
        # Update data and get results
        self.api.do_update(entity_id=entity_id,
                           values=values,
                           options=options)

    def delete(self,
               entity_id: int,
               options: dict[str, Any] = None) -> None:
        """
        Delete a row from a model using its ID

        :param entity_id: The object ID to delete
        :param options: Dictionary with options to use
        """
        if options is None:
            options = {}
        # Request data and get results
        self.api.do_delete(entity_id=entity_id,
                           options=options)

    def set_options_language(self,
                             options: dict) -> Optional[str]:
        """
        Apply the default language context to the options

        :param options: Dictionary with any existing options
        :return: The current default language code
        """
        # Set language for translated fields
        if self.api.language:
            if 'context' in options:
                options['context']['lang'] = self.api.language
            else:
                options['context'] = {'lang': self.api.language}
        return self.language

    def set_pagination(self,
                       options: dict,
                       limit: Optional[int],
                       offset: Optional[int]) -> dict:
        """
        Apply limit and offset for pagination to the options

        :param options: Dictionary with any existing options
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: The options dictionary
        """
        # Set limit and offset
        if limit is not None and 'limit' not in options:
            options['limit'] = limit
        if offset is not None and 'offset' not in options:
            options['offset'] = offset
        return options

    def get_fields(self,
                   fields: tuple[str, ...] = None,
                   attributes: list[str, ...] = None,
                   options: dict[str, Any] = None) -> Optional[dict[str, Any]]:
        """
        Get the model fields

        :param fields: List with the fields to include in the response
        :param attributes: List with the attributes to include in the response
        :param options: Dictionary with options to use
        :return: Dictionary with the requested fields
        """
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields is None:
            fields = []
        # Limit results only to selected attributes
        if attributes is not None:
            options['attributes'] = attributes
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.api.do_fields_get(fields=fields,
                                         options=options)
        return results

    @property
    def model_name(self):
        """
        Get the current model name

        :return: Model name
        """
        return self.api.model_name

    @property
    def language(self):
        """
        Get the current default language

        :return: Language code
        """
        return self.api.language

    @language.setter
    def language(self,
                 language: str):
        """
        Set the current default language

        :param language: Language code to set
        """
        self.api.language = language
