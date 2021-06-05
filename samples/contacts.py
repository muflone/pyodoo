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

from pyodoo.boolean_operator import BooleanOperator
from pyodoo.compare_type import CompareType
from pyodoo.filter import Filter
from pyodoo.v12 import Contact


# Instance object
api = Contact(endpoint=os.environ['ODOO_ENDPOINT'],
              database=os.environ['ODOO_DATABASE'],
              username=os.environ['ODOO_USERNAME'],
              password=os.environ['ODOO_PASSWORD'],
              language='it_IT')
# Authenticate
api.authenticate()

# Search some records by name
results = api.search(
    filters=[
        BooleanOperator.AND,
        Filter('name', CompareType.CONTAINS, 'Mike'),
        BooleanOperator.AND,
        BooleanOperator.NOT,
        Filter('name', CompareType.CONTAINS, 'Ross'),
        Filter('id', CompareType.NOT_EQUAL, 173806),
    ])
print('search', len(results), results)

# Find some records by ID
results = api.find(entity_ids=[24551, 24552],
                   fields=('id', 'name'))
print('find many', results)

# Find a record by ID
results = api.find(entity_ids=[24551],
                   fields=('id', 'name'))
print('find', results)

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
