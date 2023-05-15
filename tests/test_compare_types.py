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

from pyodoo import CompareType, Filter

import utility


class TestCaseCompareTypes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Model object preparation
        """
        cls.model = utility.get_model_from_demo(model_name='product.template')
        cls.model.authenticate()

    def test_01_filter_equal(self) -> None:
        """
        Search some rows using filters using compare EQUAL
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_02_filter_not_equal(self) -> None:
        """
        Search some rows using filters using compare NOT_EQUAL
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.NOT_EQUAL,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_03_filter_greater(self) -> None:
        """
        Search some rows using filters using compare GREATER
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.GREATER,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_04_filter_greater_equal(self) -> None:
        """
        Search some rows using filters using compare GREATER_EQ
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.GREATER_EQ,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly two items
        self.assertEqual(len(results), 2)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_05_filter_lower(self) -> None:
        """
        Search some rows using filters using compare LOWER
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.LOWER,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly two items
        self.assertEqual(len(results), 2)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_06_filter_lower_equal(self) -> None:
        """
        Search some rows using filters using compare LOWER_EQ
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.LOWER_EQ,
                          value='Mozzarella Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_07_filter_in(self) -> None:
        """
        Search some rows using filters using compare IN
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.IN,
                          value=('Club Sandwich', 'Mozzarella Sandwich'))]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly two items
        self.assertEqual(len(results), 2)
        # Check if the results list contains the Club Sandwich
        self.assertIn(76, results)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_08_filter_not_in(self) -> None:
        """
        Search some rows using filters using compare NOT_IN
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.NOT_IN,
                          value=('Club Sandwich', 'Mozzarella Sandwich'))]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly two items
        self.assertEqual(len(results), 2)
        # Check if the results list doesn't contain the Club Sandwich
        self.assertNotIn(76, results)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_09_filter_contains(self) -> None:
        """
        Search some rows using filters using compare CONTAINS
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly four items
        self.assertEqual(len(results), 4)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_10_filter_contains_not(self) -> None:
        """
        Search some rows using filters using compare CONTAINS_NOT
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.CONTAINS_NOT,
                          value='mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_11_filter_not_contains(self) -> None:
        """
        Search some rows using filters using compare NOT_CONTAINS
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.NOT_CONTAINS,
                          value='mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_12_filter_like(self) -> None:
        """
        Search some rows using filters using compare LIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.LIKE,
                          value='Mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_13_filter_not_like(self) -> None:
        """
        Search some rows using filters using compare NOT_LIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.NOT_LIKE,
                          value='Mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_14_filter_ilike(self) -> None:
        """
        Search some rows using filters using compare ILIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.ILIKE,
                          value='mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_15_filter_not_ilike(self) -> None:
        """
        Search some rows using filters using compare NOT_ILIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.NOT_ILIKE,
                          value='mozzarella')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly three items
        self.assertEqual(len(results), 3)
        # Check if the results list doesn't contain the Mozzarella Sandwich
        self.assertNotIn(75, results)

    def test_16_filter_raw_like(self) -> None:
        """
        Search some rows using filters using compare RAW_LIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.RAW_LIKE,
                          value='Mozzarella %')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_17_filter_raw_ilike(self) -> None:
        """
        Search some rows using filters using compare RAW_ILIKE
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='name',
                          compare_type=CompareType.RAW_ILIKE,
                          value='mozzarella %')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly one item
        self.assertEqual(len(results), 1)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_18_filter_unset_or_equal(self) -> None:
        """
        Search some rows using filters using compare UNSET_OR_EQUAL
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='uom_id',
                          compare_type=CompareType.UNSET_OR_EQUAL,
                          value=1)]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly four items
        self.assertEqual(len(results), 4)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_19_filter_child_of(self) -> None:
        """
        Search some rows using filters using compare CHILD_OF
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='categ_id',
                          compare_type=CompareType.CHILD_OF,
                          value='PoS')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly four items
        self.assertEqual(len(results), 4)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)

    def test_20_filter_parent_of(self) -> None:
        """
        Search some rows using filters using compare PARENT_OF
        """
        filters = [Filter(field='name',
                          compare_type=CompareType.CONTAINS,
                          value='Sandwich'),
                   Filter(field='categ_id',
                          compare_type=CompareType.PARENT_OF,
                          value='Food')]
        results = self.model.search(filters=filters)
        # Check if the results are not None
        self.assertIsNotNone(results)
        # Check if the results list has exactly four items
        self.assertEqual(len(results), 4)
        # Check if the results list contains the Mozzarella Sandwich
        self.assertIn(75, results)
