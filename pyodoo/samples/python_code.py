##
#     Project: PyOdoo
# Description: API for Odoo
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2025 Fabio Castelli
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

from pyodoo.v12 import PythonCode


# Check Python Code availability
print(PythonCode.is_available(endpoint=os.environ['ODOO_ENDPOINT'],
                              database=os.environ['ODOO_DATABASE'],
                              username=os.environ['ODOO_USERNAME'],
                              password=os.environ['ODOO_PASSWORD'],
                              language=None))
# Instance Python Code object
script = PythonCode(name='test script 1',
                    endpoint=os.environ['ODOO_ENDPOINT'],
                    database=os.environ['ODOO_DATABASE'],
                    username=os.environ['ODOO_USERNAME'],
                    password=os.environ['ODOO_PASSWORD'],
                    language=None)

# Get Python Code ID
print(script.id)

# Set Python Code text
print(script.set_code(text='import sys\nresult = sys.version'))

# Execute the Python code and get result
script.execute()
data = script.get_result()
print(data)

# Delete Python Code object
print(script.delete())
