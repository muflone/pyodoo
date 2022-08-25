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

import os.path
import setuptools

import pyodoo.constants


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name=pyodoo.constants.APP_NAME,
    version=pyodoo.constants.APP_VERSION,
    author=pyodoo.constants.APP_AUTHOR,
    author_email=pyodoo.constants.APP_AUTHOR_EMAIL,
    description=pyodoo.constants.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=pyodoo.constants.URL_APPLICATION,
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning ',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
