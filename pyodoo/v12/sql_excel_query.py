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

import base64
import io
from typing import Any, Optional

import pyodoo
from pyodoo.v12.model import Model

import xlrd


class SqlExcelQuery(object):
    """
    SQL Excel query to extract data from tables
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

    @staticmethod
    def is_available(endpoint: str,
                     database: str,
                     username: str,
                     password: str,
                     language: str) -> bool:
        """
        Check if the sql.excel.pdf model exists

        :param endpoint: Odoo instance endpoint
        :param database: Odoo database
        :param username: Odoo username
        :param password: User password
        :param language: Language for localizations

        :return: True if the model sql.excel.pdf exists
        """
        model = Model(model_name='ir.model',
                      endpoint=endpoint,
                      database=database,
                      username=username,
                      password=password,
                      language=language,
                      authenticate=True)
        results = model.search(
            filters=[pyodoo.Filter(field='model',
                                   compare_type=pyodoo.CompareType.EQUAL,
                                   value='sql.excel.pdf')],
            limit=1)
        return bool(results)

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

    def get_sql(self) -> Optional[str]:
        """
        Get the query SQL text

        :return: SQL text for the query
        """
        results = self.model.get(entity_id=self._query_id,
                                 fields=('id',
                                         'sql_query'))
        return results['sql_query'] if results else None

    def set_sql(self, text: str) -> bool:
        """
        Set the query SQL text

        :param text: SQL text for query
        :return: True if the query was updated
        """
        return self.model.update(entity_id=self._query_id,
                                 values={'sql_query': text})

    def set_draft(self) -> None:
        """
        Set the query object as draft
        """
        self.model.execute(method_name='action_reset_draft',
                           args=[self._query_id],
                           kwargs={},
                           ignore_none_errors=True)

    def validate(self) -> None:
        """
        Validate the query object
        """
        self.model.execute(method_name='action_validate',
                           args=[self._query_id],
                           kwargs={},
                           ignore_none_errors=False)

    def get_state(self) -> Optional[str]:
        """
        Get the query object state

        :return: the query object state
        """
        results = self.model.get(entity_id=self._query_id,
                                 fields=('state', ))
        return results['state'] if results else None

    def get_active(self) -> Optional[str]:
        """
        Get the query object active state

        :return: the query object active state
        """
        results = self.model.get(entity_id=self._query_id,
                                 fields=('active', ))
        return results['active'] if results else None

    def set_active(self, active: bool) -> bool:
        """
        Set the query object as active/inactive

        :param active: active status
        :return: True if the query was updated
        """
        return self.model.update(entity_id=self._query_id,
                                 values={'active': active})

    def execute(self) -> None:
        """
        Execute the query to create the Excel file in the `file` field

        :return: None
        """
        self.model.execute(method_name='print_xls_report',
                           args=[self._query_id],
                           kwargs={},
                           ignore_none_errors=True)
        return None

    def clear(self) -> None:
        """
        Clear the produced file
        """
        self.model.update(entity_id=self._query_id,
                          values={'file': False})

    def delete(self) -> bool:
        """
        Delete the query object

        :return: True if the query was removed
        """
        return self.model.delete(entity_id=self._query_id)

    def get_file(self) -> Optional[str]:
        """
        Get the latest produced Excel file

        :return: Excel binary file content
        """
        results = self.model.get(entity_id=self._query_id,
                                 fields=('file', ))
        if results and results['file']:
            # Decode the base64 content
            results = base64.b64decode(s=results['file'])
        else:
            results = None
        return results

    def get_data(self) -> Optional[list[dict[str, Any]]]:
        """
        Get the latest produced Excel file and extract its tabular data

        :return: list of dictionaries with data
        """
        with io.BytesIO() as file:
            file.write(self.get_file())
            with xlrd.open_workbook(file_contents=file.getvalue()) as workbook:
                worksheet = workbook.sheet_by_index(0)
                rows = worksheet.get_rows()
                # Skip the first three rows
                next(rows)
                next(rows)
                next(rows)
                # Get the column headers
                headers = [item.value
                           for item in next(rows)]
                # Get the data
                results = []
                for row in rows:
                    results.append(dict(zip(headers,
                                            [item.value for item in row])))
        return results

    def add_tag(self, tag_id: int) -> bool:
        """
        Add an existing tag to the query

        :param tag_id: Tag ID to add
        :return: True if the tag was added
        """
        return self.model.many_to_many_add(entity_id=self._query_id,
                                           field='tag_ids',
                                           related_id=tag_id)

    def get_tags(self) -> Optional[list[dict[str, Any]]]:
        """
        Get the query tags

        :return: list with the tags
        """
        if results := self.model.get(entity_id=self._query_id,
                                     fields=('id',
                                             'tag_ids')):
            model = self.model.get_model(model_name='sql.tags',
                                         authenticate=False,
                                         use_existing_uid=True)
            results = model.get_many(entity_ids=results['tag_ids'],
                                     fields=('id',
                                             'name'))
        return results or None
