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

import unittest
import xmlrpc.client

from pyodoo import (ActiveStatusChoice,
                    BooleanOperator,
                    CompareType,
                    Filter)
from pyodoo.constants import APP_NAME, APP_VERSION
from pyodoo.v12 import Model


class TestCaseContacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Model object preparation
        """
        # Get the free public server credentials
        info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
        cls.model = Model(model_name='res.partner',
                          endpoint=info['host'],
                          database=info['database'],
                          username=info['user'],
                          password=info['password'],
                          language='en_US')

    def test_01_authenticate(self) -> None:
        """
        Check the authentication
        """
        results = self.model.authenticate()
        # Check if the user ID is not None
        self.assertIsNotNone(results)
        # Check if the user ID is > 0
        self.assertGreater(results, 0)

    def test_02_all(self) -> None:
        """
        Search all the rows in the model
        """
        results = self.model.all(fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)

    def test_03_search_all(self) -> None:
        """
        Search all the rows in the model
        """
        results = self.model.search(filters=[])
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)

    def test_04_search_with_filters(self) -> None:
        """
        Search some rows using filters
        """
        # Filters by name and excluding an explicit ID
        filters = [BooleanOperator.AND,
                   Filter(field='active',
                          compare_type=CompareType.EQUAL,
                          value=False),
                   BooleanOperator.NOT,
                   Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='OdooBot'),
                   ]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list does not contain the OdooBot user ID (2)
        self.assertNotIn(2, results)

    def test_05_find_by_id_single(self) -> None:
        """
        Find a single row using its ID
        """
        results = self.model.find(entity_ids=[3],
                                  fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list contains only a single item
        self.assertEqual(len(results), 1)
        # Check some data
        self.assertEqual(results[0]['id'], 3)
        self.assertEqual(results[0]['name'], 'Mitchell Admin')
        self.assertEqual(results[0]['type'], 'contact')
        self.assertGreater(len(results[0]['street']), 0)

    def test_06_find_by_id_active(self) -> None:
        """
        Find a single active row using its ID
        """
        results = self.model.find(entity_ids=[2, 11],
                                  fields=('id', 'name', 'type', 'street'),
                                  is_active=ActiveStatusChoice.ACTIVE)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list contains only a single item
        self.assertEqual(len(results), 1)
        # Check some data
        self.assertEqual(results[0]['id'], 11)
        self.assertNotEqual(results[0]['name'], 'OdooBot')
        self.assertEqual(results[0]['type'], 'contact')
        self.assertGreater(len(results[0]['street']), 0)

    def test_07_find_by_id_inactive(self) -> None:
        """
        Find a single inactive row using its ID
        """
        results = self.model.find(entity_ids=[2, 11],
                                  fields=('id', 'name', 'type', 'street'),
                                  is_active=ActiveStatusChoice.INACTIVE)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list contains only a single item
        self.assertEqual(len(results), 1)
        # Check some data
        self.assertEqual(results[0]['id'], 2)
        self.assertEqual(results[0]['name'], 'OdooBot')
        self.assertEqual(results[0]['type'], 'contact')
        self.assertGreater(len(results[0]['street']), 0)

    def test_08_find_by_id_both_active(self) -> None:
        """
        Find two rows using their IDs, both active and inactive
        """
        results = self.model.find(entity_ids=[2, 11],
                                  fields=('id', 'name', 'type', 'street'),
                                  is_active=ActiveStatusChoice.BOTH)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list contains only a single item
        self.assertEqual(len(results), 2)
        # Check some data
        for item in results:
            self.assertIn(item['id'], (2, 11))
            self.assertEqual(item['type'], 'contact')
            self.assertGreater(len(item['street']), 0)

    def test_09_find_by_id_multiple(self) -> None:
        """
        Find multiple row using their IDs
        """
        results = self.model.find(entity_ids=[3, 15],
                                  fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list does not contain more than 2 rows
        self.assertLessEqual(len(results), 2)
        # Check if the results list contains only two items
        self.assertEqual(len(results), 2)
        # Check some data
        self.assertIn(results[0]['id'], (3, 15))

    def test_10_filter(self) -> None:
        """
        Find multiple rows using some filters
        """
        # Filters by name and excluding an explicit ID
        filters = [BooleanOperator.AND,
                   Filter(field='active',
                          compare_type=CompareType.EQUAL,
                          value=False),
                   BooleanOperator.NOT,
                   Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='OdooBot'),
                   ]
        results = self.model.filter(filters=filters,
                                    fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)

    def test_11_get(self) -> None:
        """
        Get a single row using ID
        """
        results = self.model.get(entity_id=3,
                                 fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results type is None or dict
        self.assertIn(type(results), (None, dict))
        # Check if the results is not empty
        self.assertGreater(len(results), 0)
        # Check if the results contains 4 values, for the 4 fields
        self.assertEqual(len(results), 4)
        # Check some data
        self.assertEqual(results['id'], 3)
        self.assertEqual(results['name'], 'Mitchell Admin')
        self.assertEqual(results['type'], 'contact')
        self.assertGreater(len(results['street']), 0)

    def test_12_create(self) -> None:
        """
        Create a new row
        """
        values = {'name': f'{APP_NAME} v.{APP_VERSION}'}
        results = self.model.create(values)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results is not empty
        self.assertGreater(results, 0)

    def test_13_update(self) -> None:
        """
        Update the newly created rows
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Update found data
        for entity_id in results:
            self.model.update(entity_id=entity_id,
                              values={'street': 'TEST TEST TEST'})
            results_updated = self.model.get(entity_id=entity_id,
                                             fields=('id', 'street'))
            # Check if the results are not None
            self.assertIsNotNone(results_updated)
            # Check if the results contain two fields
            self.assertEqual(len(results_updated), 2)
            # Check the field id
            self.assertEqual(results_updated['id'], entity_id)
            # Check the field street
            self.assertEqual(results_updated['street'], 'TEST TEST TEST')

    def test_14_count(self) -> None:
        """
        Count the newly created rows.
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.count(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(results, 0)

    def test_15_delete(self) -> None:
        """
        Delete the newly created rows.
        This test may be skipped in the case there's an active PoS session
        as Odoo doesn't allow contacts deletion when there's some active
        PoS session
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Delete found data
        for entity_id in results:
            try:
                self.model.delete(entity_id=entity_id)
                results_updated = self.model.get(entity_id=entity_id,
                                                 fields=('id', 'street'))
                # Check if the results are None, then deleted
                self.assertIsNone(results_updated)
            except xmlrpc.client.Fault as error:
                if error.faultCode == 2:
                    # We have an active PoS session running
                    # It's not possible to delete contacts until it's closed
                    pass
                else:
                    # We catched a different error, re-raise it
                    raise error

    def test_16_language(self) -> None:
        """
        Get the current default language, change and restore it
        """
        original_language = self.model.language
        # Check the current default language
        self.assertEqual(original_language, 'en_US')
        # Change the current default language
        self.model.language = 'it_IT'
        results = self.model.language
        # Check the current default language
        self.assertEqual(results, 'it_IT')
        # Restore the current default language
        self.model.language = original_language
        results = self.model.language
        self.assertEqual(results, original_language)
