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

import os

from pyodoo.constants import APP_NAME, APP_VERSION
from pyodoo.v12 import SqlExcelQuery


# Check SQL Excel Query availability
print(SqlExcelQuery.is_available(endpoint=os.environ['ODOO_ENDPOINT'],
                                 database=os.environ['ODOO_DATABASE'],
                                 username=os.environ['ODOO_USERNAME'],
                                 password=os.environ['ODOO_PASSWORD'],
                                 language=None))
# Instance SQL Excel Query object
query = SqlExcelQuery(name='test query 1',
                      category=f'{APP_NAME} {APP_VERSION}',
                      endpoint=os.environ['ODOO_ENDPOINT'],
                      database=os.environ['ODOO_DATABASE'],
                      username=os.environ['ODOO_USERNAME'],
                      password=os.environ['ODOO_PASSWORD'],
                      language=None)
# Change default language
query.language = 'en_GB'

# Get Query ID
print(query.id)

# Set Query SQL text
print(query.set_sql(text='SELECT\n  *\nFROM res_partner\nLIMIT 100'))

# Set and get Query state
query.set_draft()
print(query.get_state())
query.validate()
print(query.get_state())

# Set Query active status
print(query.set_active(active=False))
print(query.set_active(active=True))

# Execute the SQL query
query.execute()

# Get Excel file
data = query.get_file()

# Process the Excel file and extract its data
data = query.get_data()
print(data)

# Remove Excel file from SQL Excel Query
query.clear()

# Add query tags
query.add_tag(tag_id=4)

# Get the query tags
data = query.get_tags()
print(data)

# Delete SQL Excel Query object
print(query.delete())
