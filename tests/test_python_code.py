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

import unittest
import uuid

from pyodoo.v12 import PythonCode

import utility


class TestCasePythonCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Python Code object preparation
        """
        info = utility.get_authentication_from_demo()
        if PythonCode.is_available(endpoint=info['host'],
                                   database=info['database'],
                                   username=info['user'],
                                   password=info['password'],
                                   language='en_US'):
            # The model sql.excel.pdf is available
            cls.script_name = uuid.uuid4().hex
            cls.script = PythonCode(name=cls.script_name,
                                    endpoint=info['host'],
                                    database=info['database'],
                                    username=info['user'],
                                    password=info['password'],
                                    language='en_US')
        else:
            # The model execute.python.code is not available
            cls.script = None

    def setUp(self):
        """
        Check if the test could be run
        """
        if not self.script:
            self.skipTest('Model execute.python.code is not available')

    def test_01_get_name(self) -> None:
        """
        Check the Python Code name
        """
        results = self.script.name
        # Check if the name is not None
        self.assertIsNotNone(results)
        # Check if the name is the same
        self.assertEqual(results, self.script_name)

    def test_02_get_id(self) -> None:
        """
        Check the Python Code ID
        """
        results = self.script.id
        # Check if the ID is not None
        self.assertIsNotNone(results)
        # Check if the ID is > 0
        self.assertGreater(results, 0)

    def test_03_get_set_code(self) -> None:
        """
        Get the Python Code text
        """
        results = self.script.get_code()
        # Check if the Python Code text is not None
        self.assertIsNotNone(results)
        # Check if the Python Code text length is = 0
        self.assertEqual(len(results), 0)
        # Set new Python Code text
        python_code = ('import sys\n'
                       'result = sys.version')
        results = self.script.set_code(text=python_code)
        # Check if the response is True
        self.assertEqual(results, True)
        # Check if the Python Code text is not None
        results = self.script.get_code()
        self.assertIsNotNone(results)
        # Check if the Python Code text is the expected
        self.assertEqual(results, python_code)

    def test_04_execute(self) -> None:
        """
        Execute the Python Code
        """
        results = self.script.execute()
        # Check if the Python Code was executed
        self.assertIsNone(results)

    def test_05_get_result(self) -> None:
        """
        Get the Python Code execution results
        """
        results = self.script.get_result()
        # Check if the result is not None
        self.assertIsNotNone(results)
        # Check if the result is not empty
        self.assertGreater(len(results), 0)

    def test_06_delete(self) -> None:
        """
        Delete the Python Code
        """
        results = self.script.delete()
        # Check if the deletion was successful
        self.assertTrue(results)
