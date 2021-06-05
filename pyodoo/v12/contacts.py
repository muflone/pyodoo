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

import datetime
from typing import Any, Union

from .api import Api
from pyodoo import BooleanOperator, Filter


class Contact(Api):
    MODEL_NAME = 'res.partner'

    def get(self,
            entity_id: int,
            fields: tuple[str, ...] = None) -> dict:
        """
        Get a object from its ID

        :param entity_id: object ID to get
        :param fields: fields to include in the response
        :return: dictionary with the requested fields
        """
        return Api.get(self,
                       model=self.MODEL_NAME,
                       entity_id=entity_id,
                       fields=fields)

    def find(self,
             entity_ids: list[int],
             fields: tuple[str, ...] = None) -> list[dict]:
        """
        Find all the objects list with some ID

        :param entity_ids: objects ID to query
        :param fields: fields to include in the response
        :return: List of dictionary with the requested fields
        """
        return Api.find(self,
                        model=self.MODEL_NAME,
                        entity_ids=entity_ids,
                        fields=fields)

    def search(self,
               filters: list[Union[BooleanOperator, Filter]]) -> list[int]:
        """
        Find some objects using a list of filters

        :param filters: list of filters to used for searching the data
        :return: List of ID for the objects found
        """
        return Api.search(self,
                          model=self.MODEL_NAME,
                          filters=filters)

    def create(self,
               values: dict[str, Any]) -> int:
        """
        Create a new object

        :param values: dictionary with fields and values to update
        :return: The ID of the newly created object
        """
        return Api.create(self,
                          model=self.MODEL_NAME,
                          values=values)

    def update(self,
               entity_id: int,
               values: dict[str, Any]) -> None:
        """
        Update a object from its ID

        :param entity_id: object ID to update
        :param values: dictionary with fields and values to update
        :return: dictionary with the requested fields
        """
        Api.update(self,
                   model=self.MODEL_NAME,
                   entity_id=entity_id,
                   values=values)

    def delete(self,
               entity_id: int) -> None:
        """
        Delete a object from its ID

        :param entity_id: object ID to update
        """
        Api.delete(self,
                   model=self.MODEL_NAME,
                   entity_id=entity_id)
