##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2025 Fabio Castelli
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

from typing import Optional

import pyodoo
from pyodoo.v12.model import Model


class PythonCode(object):
    """
    Python Code to execute a Python code
    """
    def __init__(self,
                 name: str,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str
                 ) -> None:
        # Model object
        self._code_name = name
        self.model = Model(model_name='execute.python.code',
                           endpoint=endpoint,
                           database=database,
                           username=username,
                           password=password,
                           language=language,
                           authenticate=True)
        # Get or create the Python Code object
        results = self.model.search(
            filters=[pyodoo.Filter(field='name',
                                   compare_type=pyodoo.CompareType.EQUAL,
                                   value=self.name)],
            limit=1)
        if results:
            self._code_id = results[0]
        else:
            # Python Code object doesn't exist, create it right now
            self._code_id = self.model.create(values={'name': self.name,
                                                      'code': ''})

    @staticmethod
    def is_available(endpoint: str,
                     database: str,
                     username: str,
                     password: str,
                     language: str
                     ) -> bool:
        """
        Check if the execute.python.code model exists

        :param endpoint: Odoo instance endpoint
        :param database: Odoo database
        :param username: Odoo username
        :param password: User password
        :param language: Language for localizations

        :return: True if the model execute.python.code exists
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
                                   value='execute.python.code')],
            limit=1)
        return bool(results)

    @property
    def name(self
             ) -> str:
        """
        Get the current Python Code name

        :return: Python Code name
        """
        return self._code_name

    @property
    def id(self
           ) -> int:
        """
        Get the Python Code object ID
        :return: Python Code object ID
        """
        return self._code_id

    def get_code(self
                 ) -> Optional[str]:
        """
        Get the Python Code text

        :return: Python text for the Python Code
        """
        results = self.model.get(entity_id=self._code_id,
                                 fields=('id',
                                         'code'))
        return results['code'] if results else None

    def set_code(self,
                 text: str
                 ) -> bool:
        """
        Set the Python Code text

        :param text: Python text for Python Code
        :return: True if the query was updated
        """
        return self.model.update(entity_id=self._code_id,
                                 values={'code': text})

    def execute(self
                ) -> None:
        """
        Execute the Python Code

        :return: None
        """
        self.model.execute(method_name='execute_code',
                           args=[self._code_id],
                           kwargs={},
                           ignore_none_errors=False)
        return None

    def get_result(self
                   ) -> Optional[str]:
        """
        Get the latest produced result

        :return: Python Code result
        """
        results = self.model.get(entity_id=self._code_id,
                                 fields=('result', ))
        return results['result'] if results else None

    def delete(self
               ) -> bool:
        """
        Delete the Python Code object

        :return: True if the script was removed
        """
        return self.model.delete(entity_id=self._code_id)
