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

import os

from pyodoo import (BooleanOperator,
                    CompareType,
                    Filter)
from pyodoo.v12 import Model


# Instance model object
model = Model(model_name='res.partner',
              endpoint=os.environ['ODOO_ENDPOINT'],
              database=os.environ['ODOO_DATABASE'],
              username=os.environ['ODOO_USERNAME'],
              password=os.environ['ODOO_PASSWORD'],
              language=None)
# Authenticate user
model.authenticate()
# Change default language
model.language = 'en_GB'
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
results = model.search(filters=filters)
print('search', len(results), results)

# Find some records by ID
results = model.find(entity_ids=results,
                     fields=('id', 'name', 'country_id'))
print('find many', results)

# Find a record by ID
results = model.find(entity_ids=[24551],
                     fields=('id', 'name'))
print('find', results)

# Find some records by filters
results = model.filter(filters=filters,
                       fields=('id', 'name', 'country_id'))
print('filter', results)

# Get all the record
results = model.all(fields=('id', 'name'))
print('all', len(results))

# Get a record by ID
results = model.get(entity_id=24551,
                    fields=('id', 'name'))
print('get', results)

# Create a new record
entity_id = model.create(values={'firstname': 'TEST TEST TEST',
                                 'lastname': '123 456'})
print('create', entity_id)

# Update a record by ID
model.update(entity_id=entity_id,
             values={'street': 'TEST TEST TEST'})
results = model.get(entity_id=entity_id,
                    fields=('id', 'street'))
print('update', results)

# Delete a record
model.delete(entity_id=entity_id)
print('delete')

# Find customers from France with different languages
filters.append(Filter(field='lang',
                      compare_type=CompareType.NOT_EQUAL,
                      value='fr_FR'))
filters.append(Filter(field='country_id',
                      compare_type=CompareType.EQUAL,
                      value='France'))
results = model.search(filters=filters)
print('search', len(results), results)

# Update those customers to French language
for entity_id in results:
    model.update(entity_id=entity_id,
                 values={'lang': 'fr_FR'})
    print('updating ID', entity_id)
results = model.search(filters=filters)
print('search', len(results), results)
