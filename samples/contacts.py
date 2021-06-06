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

import os

from pyodoo import (BooleanOperator,
                    CompareType,
                    Filter)
from pyodoo.v12.models.res.partner import ResPartner


# Instance object
api = ResPartner(endpoint=os.environ['ODOO_ENDPOINT'],
                 database=os.environ['ODOO_DATABASE'],
                 username=os.environ['ODOO_USERNAME'],
                 password=os.environ['ODOO_PASSWORD'],
                 language='en_GB')
# Filters by name and excluding an explicit ID
filters = [BooleanOperator.AND,
           Filter(field='name',
                  compare_type=CompareType.CONTAINS,
                  value='Castelli fabio'),
           BooleanOperator.AND,
           BooleanOperator.NOT,
           Filter(field='name',
                  compare_type=CompareType.CONTAINS,
                  value='Ross'),
           Filter(field='id',
                  compare_type=CompareType.NOT_EQUAL,
                  value=173806)
           ]
# Search some records by name
results = api.search(filters=filters)
print('search', len(results), results)

# Find some records by ID
results = api.find(entity_ids=results,
                   fields=('id', 'name', 'country_id'))
print('find many', results)

# Find a record by ID
results = api.find(entity_ids=[24551],
                   fields=('id', 'name'))
print('find', results)

# Find some records by filters
results = api.filter(filters=filters,
                     fields=('id', 'name', 'country_id'))
print('filter', results)

# Get a record by ID
results = api.get(entity_id=24551,
                  fields=('id', 'name'))
print('get', results)

# Update a record by ID
api.update(entity_id=24551,
           values={'pinned_notes': 'TEST TEST TEST'})
results = api.get(entity_id=24551,
                  fields=('id', 'pinned_notes'))
print('update', results)

# Create a new record
results = api.create(values={'firstname': 'TEST TEST TEST',
                             'lastname': '123 456'})
print('create', results)

# Delete a record
api.delete(entity_id=results)
print('delete')

# Find customers from France with different languages
filters.append(Filter(field='lang',
                      compare_type=CompareType.NOT_EQUAL,
                      value='fr_FR'))
filters.append(Filter(field='country_id',
                      compare_type=CompareType.EQUAL,
                      value='France'))
results = api.search(filters=filters)
print('search', len(results), results)

# Update those customers to French language
for entity_id in results:
    api.update(entity_id=entity_id,
               values={'lang': 'fr_FR'})
    print('updating ID', entity_id)
results = api.search(filters=filters)
print('search', len(results), results)
