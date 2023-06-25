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

from pyodoo.constants import APP_NAME, APP_VERSION
from pyodoo.v12 import SqlExcelQuery

import utility


class TestCaseSqlExcelQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Query object preparation
        """
        info = utility.get_authentication_from_demo()
        if SqlExcelQuery.is_available(endpoint=info['host'],
                                      database=info['database'],
                                      username=info['user'],
                                      password=info['password'],
                                      language='en_US'):
            # The model sql.excel.pdf is available
            cls.query_name = uuid.uuid4().hex
            cls.query = SqlExcelQuery(name=cls.query_name,
                                      category=f'{APP_NAME} {APP_VERSION}',
                                      endpoint=info['host'],
                                      database=info['database'],
                                      username=info['user'],
                                      password=info['password'],
                                      language='en_US')
        else:
            # The model sql.excel.pdf is not available
            cls.query = None

    def setUp(self):
        """
        Check if the test could be run
        """
        if not self.query:
            self.skipTest('Model sql.excel.pdf is not available')

    def test_01_get_name(self) -> None:
        """
        Check the query name
        """
        results = self.query.name
        # Check if the name is not None
        self.assertIsNotNone(results)
        # Check if the name is the same
        self.assertEqual(results, self.query_name)

    def test_02_get_language(self) -> None:
        """
        Check the query language
        """
        results = self.query.language
        # Check if the language is not None
        self.assertIsNotNone(results)
        # Check if the language is the same
        self.assertEqual(results, 'en_US')

    def test_03_get_id(self) -> None:
        """
        Check the query ID
        """
        results = self.query.id
        # Check if the ID is not None
        self.assertIsNotNone(results)
        # Check if the ID is > 0
        self.assertGreater(results, 0)

    def test_04_get_set_sql(self) -> None:
        """
        Get the query SQL text
        """
        results = self.query.get_sql()
        # Check if the query SQL text is not None
        self.assertIsNotNone(results)
        # Check if the query SQL text length is = 0
        self.assertEqual(len(results), 0)
        # Set new query SQL text
        sql_text = ('SELECT customer, supplier, COUNT(*) AS count '
                    'FROM res_partner '
                    'GROUP BY customer, supplier')
        results = self.query.set_sql(text=sql_text)
        # Check if the response is True
        self.assertEqual(results, True)
        # Check if the query SQL text is not None
        results = self.query.get_sql()
        self.assertIsNotNone(results)
        # Check if the query SQL text is the expected
        self.assertEqual(results, sql_text)

    def test_05_get_state(self) -> None:
        """
        Get the query state
        """
        results = self.query.get_state()
        # Check if the query state is not None
        self.assertIsNotNone(results)
        # Check if the query state is draft
        self.assertEqual(results, 'draft')

    def test_06_validate(self) -> None:
        """
        Set the query state to validate
        """
        self.query.validate()
        # Check if the query state is not None
        results = self.query.get_state()
        self.assertIsNotNone(results)
        # Check if the query state is validate
        self.assertEqual(results, 'validate')

    def test_07_set_draft(self) -> None:
        """
        Set the query state to draft
        """
        self.query.set_draft()
        # Check if the query state is not None
        results = self.query.get_state()
        self.assertIsNotNone(results)
        # Check if the query state is draft
        self.assertEqual(results, 'draft')

    def test_08_get_set_active(self) -> None:
        """
        Get and set the query active state
        """
        # Set the query as not active
        results = self.query.set_active(active=False)
        self.assertTrue(results)
        # Check if the query active state is False
        results = self.query.get_active()
        self.assertFalse(results)
        # Set the query as active
        results = self.query.set_active(active=True)
        self.assertTrue(results)
        # Check if the query active state is True
        results = self.query.get_active()
        self.assertTrue(results)

    def test_09_execute(self) -> None:
        """
        Execute the query
        """
        results = self.query.execute()
        # Check if the query was executed
        self.assertIsNone(results)

    def test_10_get_file(self) -> None:
        """
        Get the query execution results as file
        """
        results = self.query.get_file()
        # Check if the file is not None
        self.assertIsNotNone(results)
        # Check if the file is not empty
        self.assertGreater(len(results), 0)

    def test_11_clear(self) -> None:
        """
        Clear the query execution results file
        """
        self.query.clear()
        results = self.query.get_file()
        # Check if the language is None
        self.assertIsNone(results)

    def test_12_get_data(self) -> None:
        """
        Get the query execution results as data
        """
        self.query.execute()
        results = self.query.get_data()
        # Check if the results data are not None
        self.assertIsNotNone(results)
        # Check if the results have one or more results
        self.assertGreaterEqual(len(results), 1)
        # Check if the results data have the expected fields
        self.assertIn('S.No', results[0])
        self.assertIn('customer', results[0])
        self.assertIn('supplier', results[0])
        self.assertIn('count', results[0])
        self.assertEqual(len(results[0]), 4)

    def test_13_add_tags(self) -> None:
        """
        Add and get tags from the Query
        """
        model = self.query.model.get_model(model_name='sql.tags',
                                           authenticate=False,
                                           use_existing_uid=True)
        tag_ids = model.search(filters=[])
        for tag_id in tag_ids:
            results = self.query.add_tag(tag_id=tag_id)
            # Check if the addition was successful
            self.assertTrue(results)
        # Check the resulting tags
        results = self.query.get_tags()
        # Check the tags list
        self.assertIsNotNone(results)
        results = [item['id'] for item in results]
        for tag_id in tag_ids:
            self.assertIn(tag_id, results)

    def test_14_delete(self) -> None:
        """
        Delete the query
        """
        results = self.query.delete()
        # Check if the deletion was successful
        self.assertTrue(results)
