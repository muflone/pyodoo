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
import xmlrpc.client

from pyodoo import (ActiveStatusChoice,
                    BooleanOperator,
                    CompareType,
                    Filter,
                    MessageSubType)
from pyodoo.constants import APP_AUTHOR_EMAIL, APP_NAME, APP_VERSION
from pyodoo.v12 import Model


class TestCaseContacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Model object preparation
        """
        # Get the free public server credentials
        try:
            info = xmlrpc.client.ServerProxy(
                uri='https://demo.odoo.com/start').start()
        except xmlrpc.client.Fault:
            # Sometimes the free public server start page is not available
            # Use a specif instance (this may be very mutable)
            info = {'host': 'https://demo4.odoo.com',
                    'database': 'demo_160_1676157153',
                    'user': 'admin',
                    'password': 'admin'}
        cls.model = Model(model_name='res.partner',
                          endpoint=info['host'],
                          database=info['database'],
                          username=info['user'],
                          password=info['password'],
                          language='en_US',
                          authenticate=False)

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
        results = self.model.all(fields=('id', 'name', 'type', 'street'),
                                 limit=1000)
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

    def test_04_search_all_with_options(self) -> None:
        """
        Search all the rows in the model using options with pagination
        """
        results = self.model.search(filters=[],
                                    options={'limit': 30})
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list is not greater than 30
        self.assertLessEqual(len(results), 30)

    def test_05_search_all_with_pagination(self) -> None:
        """
        Search all the rows in the model using pagination
        """
        results = self.model.search(filters=[],
                                    limit=30,
                                    offset=0)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)
        # Check if the results list is not greater than 30
        self.assertLessEqual(len(results), 30)

    def test_06_search_with_filters(self) -> None:
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

    def test_07_find_by_id_single(self) -> None:
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

    def test_08_find_by_id_active(self) -> None:
        """
        Find a single active row using its ID
        """
        results = self.model.find(entity_ids=[2, 11],
                                  is_active=ActiveStatusChoice.ACTIVE,
                                  fields=('id', 'name', 'type', 'street'))
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

    def test_09_find_by_id_inactive(self) -> None:
        """
        Find a single inactive row using its ID
        """
        results = self.model.find(entity_ids=[2, 11],
                                  is_active=ActiveStatusChoice.INACTIVE,
                                  fields=('id', 'name', 'type', 'street'))
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

    def test_10_find_by_id_both_active(self) -> None:
        """
        Find two rows using their IDs, both active and inactive
        """
        results = self.model.find(entity_ids=[2, 11],
                                  is_active=ActiveStatusChoice.BOTH,
                                  fields=('id', 'name', 'type', 'street'))
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

    def test_11_find_by_id_multiple(self) -> None:
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

    def test_12_filter(self) -> None:
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

    def test_13_filter_with_order(self) -> None:
        """
        Find multiple rows using some filters and order
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
                                    fields=('id', 'name', 'type', 'street'),
                                    order='name asc')
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list is not empty
        self.assertGreater(len(results), 0)

    def test_14_get(self) -> None:
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

    def test_15_get_many(self) -> None:
        """
        Get multiple rows using ID
        """
        results = self.model.get_many(entity_ids=[3, 4, 5],
                                      fields=('id', 'name', 'type', 'street'))
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results type is None or dict
        self.assertIn(type(results), (None, list))
        # Check if the results is not empty
        self.assertGreater(len(results), 0)
        # Check some data
        self.assertEqual(results[0]['id'], 3)
        self.assertEqual(results[0]['name'], 'Mitchell Admin')
        self.assertEqual(results[0]['type'], 'contact')
        self.assertGreater(len(results[0]['street']), 0)

    def test_16_create(self) -> None:
        """
        Create a new row
        """
        values = {'name': f'{APP_NAME} v.{APP_VERSION}'}
        results = self.model.create(values)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results is not empty
        self.assertGreater(results, 0)

    def test_17_many_to_many_add(self) -> None:
        """
        Add a record to a Many-to-Many relationship
        """
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many ADD'}
        child_contact = self.model.create(values)
        # Check if the results are not None
        self.assertIsNotNone(child_contact)
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Add the child contact to the main contact
        results = self.model.many_to_many_add(entity_id=main_contact,
                                              field='child_ids',
                                              related_id=child_contact)
        # Check if we have results
        self.assertTrue(results)

    def test_18_many_to_many_create(self) -> None:
        """
        Create a new record and add it to a Many-to-Many relationship
        """
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many CREATE'}
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Add the child contact to the main contact
        results = self.model.many_to_many_create(entity_id=main_contact,
                                                 field='child_ids',
                                                 values=values)
        # Check if we have results
        self.assertTrue(results)

    def test_19_many_to_many_update(self) -> None:
        """
        Update an existing record from a Many-to-Many relationship
        """
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Add the temporary child contact to the main contact
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many TEMP'}
        self.model.many_to_many_create(entity_id=main_contact,
                                       field='child_ids',
                                       values=values)
        # Find the child contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=values['name'])]
        results = self.model.search(filters=filters)
        child_contact = results[0] if isinstance(results, list) else results
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Update the child contact from the main contact
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many UPDATE'}
        results = self.model.many_to_many_update(entity_id=main_contact,
                                                 field='child_ids',
                                                 related_id=child_contact,
                                                 values=values)
        # Check if we have results
        self.assertTrue(results)

    def test_20_many_to_many_delete(self) -> None:
        """
        Delete an existing child record from a Many-to-Many relationship
        and delete the record itself
        """
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Add the temporary child contact to the main contact
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many TEMP'}
        self.model.many_to_many_create(entity_id=main_contact,
                                       field='child_ids',
                                       values=values)
        # Find the child contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=values['name'])]
        results = self.model.search(filters=filters)
        child_contact = results[0] if isinstance(results, list) else results
        # Check if the results are not None
        self.assertIsNotNone(results)
        try:
            # Delete the child contact from the main contact
            results = self.model.many_to_many_delete(entity_id=main_contact,
                                                     field='child_ids',
                                                     related_id=child_contact)
            # Check if we have results
            self.assertTrue(results)
        except xmlrpc.client.Fault as error:
            if error.faultCode == 2:
                # We have an active PoS session running
                # It's not possible to delete contacts until it's closed
                pass
            else:
                # We catched a different error, re-raise it
                raise error

    def test_21_many_to_many_remove(self) -> None:
        """
        Remove an existing child record from a Many-to-Many relationship
        """
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Add the temporary child contact to the main contact
        values = {'name': f'{APP_NAME} v.{APP_VERSION} Many-to-Many REMOVED'}
        self.model.many_to_many_create(entity_id=main_contact,
                                       field='child_ids',
                                       values=values)
        # Find the child contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=values['name'])]
        results = self.model.search(filters=filters)
        child_contact = results[0] if isinstance(results, list) else results
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Remove the child contact from the main contact
        results = self.model.many_to_many_remove(entity_id=main_contact,
                                                 field='child_ids',
                                                 related_id=child_contact)
        # Check if we have results
        self.assertTrue(results)

    def test_22_many_to_many_clear(self) -> None:
        """
        Clear any existing children records from a Many-to-Many relationship
        """
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Remove any children contacts from the main contact
        results = self.model.many_to_many_clear(entity_id=main_contact,
                                                field='child_ids')
        # Check if we have results
        self.assertTrue(results)

    def test_23_many_to_many_replace(self) -> None:
        """
        Replace any existing children records from a Many-to-Many relationship
        """
        # Find the main contact
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        main_contact = results[0] if isinstance(results, list) else results
        # Find the children records to replace
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value=f'{APP_NAME} v.{APP_VERSION}'),
                   Filter(field='id',
                          compare_type=CompareType.NOT_EQUAL,
                          value=main_contact)]
        contacts = self.model.search(filters=filters)
        self.assertIsNotNone(contacts)
        self.assertNotIn(main_contact, contacts)
        # Replace any children contacts from the main contact
        results = self.model.many_to_many_replace(entity_id=main_contact,
                                                  field='child_ids',
                                                  related_ids=contacts)
        # Check if we have results
        self.assertTrue(results)

    def test_24_update(self) -> None:
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
                              values={'street': 'TEST TEST TEST',
                                      'email': APP_AUTHOR_EMAIL})
            results_updated = self.model.get(entity_id=entity_id,
                                             fields=('id', 'email', 'street'))
            # Check if the results are not None
            self.assertIsNotNone(results_updated)
            # Check if the results contain two fields
            self.assertEqual(len(results_updated), 3)
            # Check the field id
            self.assertEqual(results_updated['id'], entity_id)
            # Check the field email
            self.assertEqual(results_updated['email'], APP_AUTHOR_EMAIL)
            # Check the field street
            self.assertEqual(results_updated['street'], 'TEST TEST TEST')

    def test_25_update_many(self) -> None:
        """
        Update all the newly created rows at once
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Update found data
        self.model.update(entity_id=results,
                          values={'street': 'TEST TEST TEST 2'})

    def test_26_count(self) -> None:
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

    def test_27_get_model_data_reference(self) -> None:
        """
        Get a reference row from ir.model.data
        """
        results = self.model.get_model_data_reference(
            module_name='mail',
            value=MessageSubType.COMMENT)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, dict)
        self.assertGreater(results['res_id'], 0)

    def test_28_get_message_subtype_id_activity(self) -> None:
        """
        Get a Message subtype ID
        """
        results = self.model.get_message_subtype_id(
            subtype=MessageSubType.ACTIVITY)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, int)
        self.assertGreater(results, 0)

    def test_29_get_message_subtype_id_comment(self) -> None:
        """
        Get a Message subtype ID
        """
        results = self.model.get_message_subtype_id(
            subtype=MessageSubType.COMMENT)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, int)
        self.assertGreater(results, 0)

    def test_30_get_message_subtype_id_note(self) -> None:
        """
        Get a Message subtype ID
        """
        results = self.model.get_message_subtype_id(
            subtype=MessageSubType.NOTE)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, int)
        self.assertGreater(results, 0)

    def test_31_post_message_activity(self) -> None:
        """
        Post a new message as activity
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Add a comment
        entity_id = self.model.post_message_as_activity(
            entity_id=results[0],
            body='This is an activity message',
            author_id=results[0])
        self.assertIsNotNone(entity_id)
        self.assertGreater(entity_id, 0)

    def test_32_post_message_comment(self) -> None:
        """
        Post a new message as comment
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Add a comment
        entity_id = self.model.post_message_as_comment(
            entity_id=results[0],
            body='This is a comment message',
            author_id=results[0])
        self.assertIsNotNone(entity_id)
        self.assertGreater(entity_id, 0)

    def test_33_post_message_note(self) -> None:
        """
        Post a new message as note
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        results = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        # Add a comment
        entity_id = self.model.post_message_as_note(
            entity_id=results[0],
            body='This is a note message',
            author_id=results[0])
        self.assertIsNotNone(entity_id)
        self.assertGreater(entity_id, 0)

    def test_34_delete(self) -> None:
        """
        Delete the newly created rows.
        This test may be skipped in the case there's an active PoS session
        as Odoo doesn't allow contacts deletion when there's some active
        PoS session
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        contacts = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(contacts)
        self.assertGreater(len(contacts), 0)
        # Delete found data
        if contacts:
            entity_id = contacts[0]
            try:
                results = self.model.delete(entity_id=entity_id)
                self.assertTrue(results)
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

    def test_35_delete_many(self) -> None:
        """
        Delete the newly created rows.
        This test may be skipped in the case there's an active PoS session
        as Odoo doesn't allow contacts deletion when there's some active
        PoS session
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value=f'{APP_NAME} v.{APP_VERSION}')]
        contacts = self.model.search(filters=filters)
        # Check if we have results
        self.assertIsNotNone(contacts)
        # Delete found data
        try:
            results = self.model.delete(entity_id=contacts)
            self.assertTrue(results)
        except xmlrpc.client.Fault as error:
            if error.faultCode == 2:
                # We have an active PoS session running
                # It's not possible to delete contacts until it's closed
                pass
            else:
                # We catched a different error, re-raise it
                raise error

    def test_36_language(self) -> None:
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

    def test_37_get_fields(self) -> None:
        """
        Get the model fields
        """
        results = self.model.get_fields()
        # Check if we have results
        self.assertIsNotNone(results)

    def test_38_get_fields_attributes(self) -> None:
        """
        Get the model fields
        """
        results = self.model.get_fields(attributes=['string', 'type'])
        # Check if we have results
        self.assertIsNotNone(results)
        # Check if we have 2 fields
        field_name = results['name']
        self.assertEqual(len(field_name), 2)
        self.assertIn('string', field_name)
        self.assertIn('type', field_name)

    def test_39_get_model(self) -> None:
        """
        Get a new Model object
        """
        model_name = 'res.users'
        results = self.model.get_model(model_name=model_name,
                                       authenticate=False)
        # Check if we have results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, Model)
        self.assertEqual(results.model_name, model_name)
