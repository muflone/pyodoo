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

from .api import Api


class Contact(Api):
    def find_by_id(self,
                   entity_id: int,
                   fields: tuple[str] = None) -> dict:
        """
        Get a contact from its ID
        :param ids: contact id to query
        :param fields: fields to include in the response
        :return: dictionary with the requested fields
        """
        results = self.list_items(ids=[entity_id],
                                  fields=fields)
        return results[0] if results else None

    def list_items(self,
                   ids: tuple[int],
                   fields: tuple[str] = None) -> list[dict]:
        """
        Get a contacts list from ID
        :param ids: contacts id to query
        :param fields: fields to include in the response
        :return: List of dictionary with the requested fields
        """
        filter = [[]]
        # Add filtered IDs
        if ids:
            filter[0].append(['id', 'in', ids])
        options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self.set_options_language(options=options)
        # Request data and get results
        results = self.search_read(model='res.partner',
                                   filter=filter,
                                   options=options)
        return results if results else None
