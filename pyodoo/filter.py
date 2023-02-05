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

from typing import Union

from pyodoo import CompareType


class Filter(object):
    """
    A filter object used by Odoo
    """
    def __init__(self,
                 field: str,
                 compare_type: CompareType,
                 value: object):
        self.field = field
        self.compare_type = compare_type
        self.value = value

    def explode(self) -> list[Union[str, object]]:
        """
        Extract the list from the filter, in the format used in Odoo filters

        :return: list with three values (field name, compare type and value)
        """
        return [self.field,
                self.compare_type,
                self.value]
