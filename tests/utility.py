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
import xmlrpc.client

from pyodoo.v12 import Model


def get_authentication_from_demo() -> dict[str, str]:
    """
    Get the authentication information from the public demo server

    :return: dictionary with authentication information
    """
    try:
        # Use the environment variables
        info = {'host': os.environ['ODOO_ENDPOINT'],
                'database': os.environ['ODOO_DATABASE'],
                'user': os.environ['ODOO_USERNAME'],
                'password': os.environ['ODOO_PASSWORD']}
    except KeyError:
        try:
            # Get the free public server credentials
            info = xmlrpc.client.ServerProxy(
                uri='https://demo.odoo.com/start').start()
        except (xmlrpc.client.Fault,
                xmlrpc.client.ProtocolError):
            # Sometimes the free public server start page is not available
            # Use a specif instance (this may be very mutable)
            info = {'host': 'https://demo6.odoo.com',
                    'database': 'demo_saas-163_ffb2db7c8faa_1687302108',
                    'user': 'admin',
                    'password': 'admin'}
    return info

def get_model_from_demo(model_name: str):
    """
    Get a Model object from the public demo server

    :param model_name: name of the model to instance
    :return: pyodoo Model object
    """
    info = get_authentication_from_demo()
    return Model(model_name=model_name,
                 endpoint=info['host'],
                 database=info['database'],
                 username=info['user'],
                 password=info['password'],
                 language='en_US',
                 authenticate=False)
