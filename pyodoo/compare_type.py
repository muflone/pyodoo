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

class CompareType(object):
    """
    Comparison types used in Odoo filters
    """
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER = '>'
    GREATER_EQ = '>='
    LOWER = '<'
    LOWER_EQ = '<='
    IN = 'in'
    NOT_IN = 'not in'
    CONTAINS = 'ilike'
    CONTAINS_NOT = 'not ilike'
