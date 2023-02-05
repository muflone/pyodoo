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

import asyncio
import datetime
import os
import time

from pyodoo.v12 import Model

from awaitable import awaitable


def measure_time(name: str, start: float) -> None:
    """
    Print elapsed time since start time

    :param name: task name
    :param start: start time
    """
    duration = int((time.time() - start) * 1000)
    print(f'Duration for {name}: {duration} ms')


def update_many(minimum: int, maximum: int) -> None:
    for i in range(minimum, maximum):
        update_one(i)


def update_one(entity_id: int) -> None:
    now = datetime.datetime.now().strftime('%d/%M/%Y %H:%m.%S')
    model.update(entity_id=entity_id,
                 values={'name': f'test {now}'})


async def update_many_async(minimum: int, maximum: int) -> None:
    tasks = []
    for i in range(minimum, maximum):
        tasks.append(update_one_async(i))
    await asyncio.gather(*tasks)


@awaitable
def update_one_async(entity_id: int) -> None:
    now = datetime.datetime.now().strftime('%d/%M/%Y %H:%m.%S')
    model.update(entity_id=entity_id,
                 values={'name': f'test {now}'})


def find_many(entity_ids: list[int]) -> list[list[dict[str, str]]]:
    results = []
    for entity_id in entity_ids:
        results.append(find_one([entity_id]))
    return results


def find_one(entity_ids: list[int]) -> list[dict[str, str]]:
    results = model.find(entity_ids=entity_ids,
                         fields=('id', 'name', 'country_id'))
    return results


async def find_many_async(entity_ids: list[int]) -> None:
    tasks = []
    for entity_id in entity_ids:
        tasks.append(find_one_async([entity_id]))
    results = await asyncio.gather(*tasks)
    return results


@awaitable
def find_one_async(entity_ids: list[int]) -> list[dict[str, str]]:
    results = model.find(entity_ids=entity_ids,
                         fields=('id', 'name', 'country_id'))
    return results


# Instance model object
model = Model(model_name='res.partner',
              endpoint=os.environ['ODOO_ENDPOINT'],
              database=os.environ['ODOO_DATABASE'],
              username=os.environ['ODOO_USERNAME'],
              password=os.environ['ODOO_PASSWORD'],
              language=None,
              authenticate=False)
# Authenticate user
model.authenticate()
# Change default language
model.language = 'en_GB'

start_time = time.time()
find_many(list(range(24540, 24550)))
measure_time(name='find_many', start=start_time)

start_time = time.time()
asyncio.run(find_many_async(list(range(24540, 24550))))
measure_time(name='find_many_async', start=start_time)

start_time = time.time()
update_many(minimum=24540, maximum=24550)
measure_time(name='update_many', start=start_time)

start_time = time.time()
asyncio.run(update_many_async(minimum=24540, maximum=24550))
measure_time(name='update_many_async', start=start_time)
