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

from pyodoo.v12 import Contact


# Instance object
api = Contact(endpoint=os.environ['ODOO_ENDPOINT'],
              database=os.environ['ODOO_DATABASE'],
              username=os.environ['ODOO_USERNAME'],
              password=os.environ['ODOO_PASSWORD'],
              language='it_IT')
# Authenticate
api.authenticate()
# List some records by ID
results = api.list_items(ids=(24551, 24552),
                         fields=('id', 'name'))
print(results)
# Find a record by ID
results = api.find_by_id(entity_id=24551,
                         fields=('id', 'name'))
print(results)
