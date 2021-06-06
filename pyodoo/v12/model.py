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

from typing import Any, Union

from .api import Api
from pyodoo import BooleanOperator, Filter


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
        # Associate model
        if not model_name:
            raise NotImplementedError('model name was not set properly')
        self.model_name = model_name
        # API object
        self.api = Api(model_name=model_name,
                       endpoint=endpoint,
                       database=database,
                       username=username,
                       password=password,
                       language=language)
        self.api.authenticate()

    def get(self,
            entity_id: int,
            fields: tuple[str, ...] = None) -> dict:
        """
        Get a object from its ID

        :param entity_id: Object ID to get
        :param fields: Fields to include in the response
        :return: Dictionary with the requested fields
        """
        return self.api.get(entity_id=entity_id,
                            fields=fields)

    def find(self,
             entity_ids: list[int],
             fields: tuple[str, ...] = None) -> list[dict]:
        """
        Find all the objects list with some ID

        :param entity_ids: Objects ID to query
        :param fields: Fields to include in the response
        :return: List of dictionary with the requested fields
        """
        return self.api.find(entity_ids=entity_ids,
                             fields=fields)

    def filter(self,
               filters: list[Union[BooleanOperator, Filter]],
               fields: tuple[str, ...] = None) -> list[dict]:
        """
        Find some objects using a list of filters

        :param filters: List of filters to used for searching the data
        :param fields: Fields to include in the response
        :return: List of dictionary with the requested fields
        """
        return self.api.filter(filters=filters,
                               fields=fields)

    def search(self,
               filters: list[Union[BooleanOperator, Filter]]) -> list[int]:
        """
        Find some objects using a list of filters

        :param filters: List of filters to used for searching the data
        :return: List of ID for the objects found
        """
        return self.api.search(filters=filters)

    def create(self,
               values: dict[str, Any]) -> int:
        """
        Create a new object

        :param values: Dictionary with fields and values to update
        :return: The ID of the newly created object
        """
        return self.api.create(values=values)

    def update(self,
               entity_id: int,
               values: dict[str, Any]) -> None:
        """
        Update a object from its ID

        :param entity_id: Object ID to update
        :param values: Dictionary with fields and values to update
        :return: Dictionary with the requested fields
        """
        self.api.update(entity_id=entity_id,
                        values=values)

    def delete(self,
               entity_id: int) -> None:
        """
        Delete a object from its ID

        :param entity_id: Object ID to update
        """
        self.api.delete(entity_id=entity_id)
