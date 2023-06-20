##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2023 Fabio Castelli
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

import pyodoo
from pyodoo.v12.model import Model


class Query(object):
    """
    SQL query to extract data from tables
    """
    def __init__(self,
                 name: str,
                 category: str,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str):
        # Model object
        self._query_name = name
        self.model = Model(model_name='sql.excel.pdf',
                           endpoint=endpoint,
                           database=database,
                           username=username,
                           password=password,
                           language=language,
                           authenticate=True)
        # Get or create the category ID
        model_category = self.model.get_model(model_name='sql.category',
                                              authenticate=False,
                                              use_existing_uid=True)
        results = model_category.search(
            filters=[pyodoo.Filter(field='name',
                                   compare_type=pyodoo.CompareType.EQUAL,
                                   value=category)],
            limit=1)
        if results:
            category_id = results[0]
        else:
            category_id = model_category.create(values={'name': category})
        # Get or create the query object
        results = self.model.search(
            filters=[pyodoo.Filter(field='name',
                                   compare_type=pyodoo.CompareType.EQUAL,
                                   value=self.name)],
            is_active=pyodoo.ActiveStatusChoice.BOTH,
            limit=1)
        if results:
            self._query_id = results[0]
        else:
            # Query object doesn't exist, create it right now
            self._query_id = self.model.create(
                values={'name': self.name,
                        'category_id': category_id,
                        'sql_query': ''})

    @property
    def name(self) -> str:
        """
        Get the current query name

        :return: Query name
        """
        return self._query_name

    @property
    def language(self) -> str:
        """
        Get the current default language

        :return: Language code
        """
        return self.model.language

    @language.setter
    def language(self,
                 language: str):
        """
        Set the current default language

        :param language: Language code to set
        """
        self.model.language = language

    @property
    def id(self) -> int:
        """
        Get the query object ID
        :return: query object ID
        """
        return self._query_id
