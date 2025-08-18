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

import functools
from typing import Any, Optional, Union
import xmlrpc

from pyodoo import (ActiveStatusChoice,
                    BooleanOperator,
                    CompareType,
                    Filter,
                    MessageSubType)
from pyodoo.v12.api import Api


class Model(object):
    """
    Generic data model to interact with Odoo data models.
    """
    def __init__(self,
                 model_name: str,
                 endpoint: str,
                 database: str,
                 username: str,
                 password: str,
                 language: str = None,
                 authenticate: bool = False
                 ) -> None:
        # API object
        self.api = Api(model_name=model_name,
                       endpoint=endpoint,
                       database=database,
                       username=username,
                       password=password,
                       language=language)
        # Message Subtype IDs
        self._message_subtypes = {}
        # Automatically authenticate if required
        if authenticate:
            self.authenticate()

    def _ignore_none_errors(func):
        """
        Decorator to ignore XML-RPC None errors

        Passing the `ignore_none_errors` argument to the decorated function
        then the None errors, unacceptable for XMLRPC, will be ignored and,
        in the case the decorated function will return None, a default None
        value will be instead returned (use with cautions).
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ignore_none_errors: bool = kwargs.pop('ignore_none_errors', False)
            try:
                result = func(*args, **kwargs)
            except xmlrpc.client.Fault as error:
                none_message = ('cannot marshal None unless '
                                'allow_none is enabled')
                if (ignore_none_errors and
                        error.faultCode == 1 and
                        none_message in error.faultString):
                    # Ignore errors about None
                    result = None
                else:
                    raise
            return result
        return wrapper

    def _set_active(self,
                    filters: list[Union[BooleanOperator, Filter]],
                    is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
                    ) -> None:
        """
        Add a new filter for active records

        :param filters: List of filters used for searching the data
        :return: None
        """
        if filters is not None:
            if is_active == ActiveStatusChoice.BOTH:
                filters.append(['active', CompareType.IN, is_active])
            elif is_active != ActiveStatusChoice.NOT_SET:
                filters.append(['active', CompareType.EQUAL, is_active])

    def _set_options_language(self,
                              options: dict
                              ) -> Optional[str]:
        """
        Apply the default language context to the options

        :param options: Dictionary with any existing options
        :return: The current default language code
        """
        # Set language for translated fields
        if self.api.language:
            if 'context' in options:
                options['context']['lang'] = self.api.language
            else:
                options['context'] = {'lang': self.api.language}
        return self.language

    def _set_order_by(self,
                      options: dict,
                      order: Optional[str]
                      ) -> dict:
        """
        Apply order for ordering results to the options

        :param options: Dictionary with any existing options
        :param order: Order string
        :return: The options dictionary
        """
        # Set order
        if order is not None and 'order' not in options:
            options['order'] = order
        return options

    def _set_pagination(self,
                        options: dict,
                        limit: Optional[int],
                        offset: Optional[int]
                        ) -> dict:
        """
        Apply limit and offset for pagination to the options

        :param options: Dictionary with any existing options
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :return: The options dictionary
        """
        # Set limit and offset
        if limit is not None and 'limit' not in options:
            options['limit'] = limit
        if offset is not None and 'offset' not in options:
            options['offset'] = offset
        return options

    @property
    def model_name(self
                   ) -> str:
        """
        Get the current model name

        :return: Model name
        """
        return self.api.model_name

    @property
    def language(self
                 ) -> str:
        """
        Get the current default language

        :return: Language code
        """
        return self.api.language

    @language.setter
    def language(self,
                 language: str
                 ) -> None:
        """
        Set the current default language

        :param language: Language code to set
        """
        self.api.language = language

    def authenticate(self
                     ) -> int:
        """
        Authenticate the session using database, username and password.

        :return: The user ID for the authenticated user
        """
        return self.api.authenticate()

    def get_model(self,
                  model_name: str,
                  authenticate: bool = False,
                  use_existing_uid: bool = False
                  ) -> 'Model':
        """
        Get a Model object for another model name
        :param model_name: Model name
        :param authenticate: Automatically authenticate user
        :param use_existing_uid: Use the existing UID if not authenticated
        :return: Model object
        """
        model = Model(model_name=model_name,
                      endpoint=self.api.endpoint,
                      database=self.api.database,
                      username=self.api.username,
                      password=self.api.password,
                      language=self.api.language,
                      authenticate=authenticate)
        if not authenticate and use_existing_uid:
            # Use the existing UID
            model.api.uid = self.api.uid
        return model

    @_ignore_none_errors
    def get_model_data_reference(self,
                                 module_name: str,
                                 value: str,
                                 ignore_none_errors: bool = False
                                 ) -> Any:
        """
        Get a reference row from ir.module.data

        :param module_name: Module name to lookup
        :param value: Value to lookup
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Dictionary with the data for the referenced object
        """
        model = self.get_model(model_name='ir.model.data',
                               authenticate=True)
        filters = [Filter(field='module',
                          compare_type=CompareType.EQUAL,
                          value=module_name),
                   Filter(field='name',
                          compare_type=CompareType.EQUAL,
                          value=value)]
        options = {}
        model._set_pagination(options=options,
                              limit=1,
                              offset=0)
        results = model.filter(filters=filters,
                               fields=(),
                               options={},
                               limit=1,
                               offset=0)
        return results[0] if results else None

    @_ignore_none_errors
    def get(self,
            entity_id: int,
            fields: tuple[str, ...] = None,
            options: dict[str, Any] = None,
            ignore_none_errors: bool = False
            ) -> Optional[dict[str, Any]]:
        """
        Get a row from a model using its ID

        :param entity_id: Object ID to query
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Dictionary with the requested fields
        """
        results = self.get_many(entity_ids=[entity_id],
                                fields=fields,
                                options=options)
        return results[0] if results else None

    @_ignore_none_errors
    def get_many(self,
                 entity_ids: list[int],
                 fields: tuple[str, ...] = None,
                 options: dict[str, Any] = None,
                 ignore_none_errors: bool = False
                 ) -> Optional[list[dict[str, Any]]]:
        """
        Get a row from a model using its ID

        :param entity_ids: Object IDs to query
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of dictionaries with the requested fields
        """
        # Set options
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self._set_options_language(options=options)
        # Request data and get results
        results = self.api.do_read_many(entity_ids=entity_ids,
                                        options=options)
        return results

    @_ignore_none_errors
    def all(self,
            is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
            fields: tuple[str, ...] = None,
            options: dict[str, Any] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            order: Optional[str] = None,
            ignore_none_errors: bool = False
            ) -> list[dict[str, Any]]:
        """
        Get all the objects

        :param is_active: Additional filter for active field
        :param fields: Fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :param order: Ordering clause
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of dictionaries with the requested fields
        """
        return self.filter(filters=[],
                           is_active=is_active,
                           fields=fields,
                           options=options,
                           limit=limit,
                           offset=offset,
                           order=order)

    @_ignore_none_errors
    def find(self,
             entity_ids: list[int],
             is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
             fields: tuple[str, ...] = None,
             options: dict[str, Any] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None,
             order: Optional[str] = None,
             ignore_none_errors: bool = False
             ) -> list[dict[str, Any]]:
        """
        Find some rows from a model using their ID

        :param entity_ids: Objects ID to query
        :param is_active: Additional filter for active field
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :param order: Ordering clause
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of dictionaries with the requested fields
        """
        # Add filtered IDs
        filters = [['id', CompareType.IN, entity_ids]]
        # Filter for active status
        self._set_active(filters=filters,
                         is_active=is_active)
        # Set options
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self._set_options_language(options=options)
        # Set pagination
        self._set_pagination(options=options,
                             limit=limit,
                             offset=offset)
        # Set order
        self._set_order_by(options=options,
                           order=order)
        # Request data and get results
        results = self.api.do_search_read(filters=filters,
                                          options=options)
        return results

    @_ignore_none_errors
    def filter(self,
               filters: list[Union[BooleanOperator, Filter]],
               is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
               fields: tuple[str, ...] = None,
               options: dict[str, Any] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None,
               order: Optional[str] = None,
               ignore_none_errors: bool = False
               ) -> list[dict[str, Any]]:
        """
        Find some rows from a model using some filters

        :param filters: List of filters used for searching the data
        :param is_active: Additional filter for active field
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :param order: Ordering clause
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of dictionaries with the requested fields
        """
        # Filter for active status
        self._set_active(filters=filters,
                         is_active=is_active)
        # Set options
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields:
            options['fields'] = fields
        # Set language for translated fields
        self._set_options_language(options=options)
        # Set pagination
        self._set_pagination(options=options,
                             limit=limit,
                             offset=offset)
        # Set order
        self._set_order_by(options=options,
                           order=order)
        # Request data and get results
        results = self.api.do_search_read(filters=filters,
                                          options=options)
        return results

    @_ignore_none_errors
    def first(self,
              filters: list[Union[BooleanOperator, Filter]],
              is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
              fields: tuple[str, ...] = None,
              options: dict[str, Any] = None,
              limit: Optional[int] = None,
              offset: Optional[int] = None,
              order: Optional[str] = None,
              ignore_none_errors: bool = False
              ) -> Optional[dict[str, Any]]:
        """
        Find the first row from a model using some filters

        :param filters: List of filters used for searching the data
        :param is_active: Additional filter for active field
        :param fields: Tuple with the fields to include in the response
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :param order: Ordering clause
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of dictionaries with the requested fields
        """
        results = self.filter(filters=filters,
                              is_active=is_active,
                              fields=fields,
                              options=options,
                              limit=limit,
                              offset=offset,
                              order=order)
        return results[0] if results else None

    @_ignore_none_errors
    def count(self,
              filters: list[Union[BooleanOperator, Filter]],
              is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
              options: dict[str, Any] = None,
              ignore_none_errors: bool = False
              ) -> int:
        """
        Get the rows count from a model using some filters

        :param filters: List of filters used for searching the data
        :param is_active: Additional filter for active field
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Rows count
        """
        # Filter for active status
        self._set_active(filters=filters,
                         is_active=is_active)
        # Set options
        if options is None:
            options = {}
        # Request data and get results
        results = self.api.do_search_count(filters=filters,
                                           options=options)
        return results

    @_ignore_none_errors
    def search(self,
               filters: list[Union[BooleanOperator, Filter]],
               is_active: ActiveStatusChoice = ActiveStatusChoice.NOT_SET,
               options: dict[str, Any] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None,
               order: Optional[str] = None,
               ignore_none_errors: bool = False
               ) -> list[int]:
        """
        Find rows list from a list of filters

        :param filters: List of filters used for searching the data
        :param is_active: Additional filter for active field
        :param options: Dictionary with options to use
        :param limit: Maximum number of results count
        :param offset: Starting record number to fetch the data
        :param order: Ordering clause
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: List of ID for the objects found
        """
        # Filter for active status
        self._set_active(filters=filters,
                         is_active=is_active)
        # Set options
        if options is None:
            options = {}
        # Set language for translated fields
        self._set_options_language(options=options)
        # Set pagination
        self._set_pagination(options=options,
                             limit=limit,
                             offset=offset)
        # Set order
        self._set_order_by(options=options,
                           order=order)
        # Request data and get results
        results = self.api.do_search(filters=filters,
                                     options=options)
        return results

    @_ignore_none_errors
    def create(self,
               values: dict[str, Any],
               options: dict[str, Any] = None,
               ignore_none_errors: bool = False
               ) -> int:
        """
        Create a new record in the requested model and returns its ID

        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: The ID of the newly created object
        """
        # Set options
        if options is None:
            options = {}
        # Set language for translated fields
        self._set_options_language(options=options)
        # Create data and get results
        results = self.api.do_create(values=values,
                                     options=options)
        return results

    @_ignore_none_errors
    def update(self,
               entity_id: Union[int, list[int]],
               values: dict[str, Any],
               options: dict[str, Any] = None,
               ignore_none_errors: bool = False
               ) -> bool:
        """
        Update one or multiple rows from a model using the object IDs

        :param entity_id: The object IDs to update
        :param values: Dictionary with the fields to update and their values
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the records were updated
        """
        # Set options
        if options is None:
            options = {}
        # Set language for translated fields
        self._set_options_language(options=options)
        # Update data and get results
        results = self.api.do_update(entity_id=entity_id,
                                     values=values,
                                     options=options)
        return results

    @_ignore_none_errors
    def delete(self,
               entity_id: Union[int, list[int]],
               options: dict[str, Any] = None,
               ignore_none_errors: bool = False
               ) -> bool:
        """
        Delete one or multiple rows from a model using the object IDs

        :param entity_id: The object IDs to delete
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the records were deleted
        """
        # Set options
        if options is None:
            options = {}
        # Request data and get results
        results = self.api.do_delete(entity_id=entity_id,
                                     options=options)
        return results

    @_ignore_none_errors
    def get_fields(self,
                   fields: tuple[str, ...] = None,
                   attributes: list[str, ...] = None,
                   options: dict[str, Any] = None,
                   ignore_none_errors: bool = False
                   ) -> Optional[dict[str, Any]]:
        """
        Get the model fields

        :param fields: List with the fields to include in the response
        :param attributes: List with the attributes to include in the response
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Dictionary with the requested fields
        """
        # Set options
        if options is None:
            options = {}
        # Limit results only to selected fields
        if fields is None:
            fields = []
        # Limit results only to selected attributes
        if attributes is not None:
            options['attributes'] = attributes
        # Set language for translated fields
        self._set_options_language(options=options)
        # Request data and get results
        results = self.api.do_fields_get(fields=fields,
                                         options=options)
        return results

    @_ignore_none_errors
    def many_to_many_create(self,
                            entity_id: int,
                            field: str,
                            values: dict[str, Any],
                            options: dict[str, Any] = None,
                            ignore_none_errors: bool = False
                            ) -> bool:
        """
        Create a new object and add it to a Many-to-Many relationship

        :param entity_id: The object ID to update
        :param field: The field name for the relationship to update
        :param values: Dictionary with values for the new record to create
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was updated
        """
        return self.update(entity_id=entity_id,
                           values={field: [(0, 0, values)]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_add(self,
                         entity_id: int,
                         field: str,
                         related_id: int,
                         options: dict[str, Any] = None,
                         ignore_none_errors: bool = False
                         ) -> bool:
        """
        Add an existing related object to a Many-to-Many relationship

        :param entity_id: The object ID to update
        :param field: The field name for the relationship to update
        :param related_id: The object ID to add
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was updated
        """
        return self.update(entity_id=entity_id,
                           values={field: [(4, related_id)]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_update(self,
                            entity_id: int,
                            field: str,
                            related_id: int,
                            values: dict[str, Any],
                            options: dict[str, Any] = None,
                            ignore_none_errors: bool = False
                            ) -> bool:
        """
        Update an existing related object from a Many-to-Many relationship

        :param entity_id: The object ID to update
        :param field: The field name for the relationship to update
        :param related_id: The object ID to add
        :param values: Dictionary with values for the record to update
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was updated
        """
        return self.update(entity_id=entity_id,
                           values={field: [(1, related_id, values)]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_delete(self,
                            entity_id: int,
                            field: str,
                            related_id: int,
                            options: dict[str, Any] = None,
                            ignore_none_errors: bool = False
                            ) -> bool:
        """
        Delete an existing related object from a Many-to-Many relationship
        and delete the whole object completely

        :param entity_id: The object ID from which delete the related object
        :param field: The field name for the relationship to update
        :param related_id: The object ID to delete
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was deleted
        """
        return self.update(entity_id=entity_id,
                           values={field: [(2, related_id)]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_remove(self,
                            entity_id: int,
                            field: str,
                            related_id: int,
                            options: dict[str, Any] = None,
                            ignore_none_errors: bool = False
                            ) -> bool:
        """
        Remove an existing related object from a Many-to-Many relationship

        :param entity_id: The object ID from which remove the related object
        :param field: The field name for the relationship to update
        :param related_id: The object ID to remove
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was removed
        """
        return self.update(entity_id=entity_id,
                           values={field: [(3, related_id)]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_clear(self,
                           entity_id: int,
                           field: str,
                           options: dict[str, Any] = None,
                           ignore_none_errors: bool = False
                           ) -> bool:
        """
        Clear any existing related objects from a Many-to-Many relationship

        :param entity_id: The object ID from which remove the related object
        :param field: The field name for the relationship to update
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was updated
        """
        return self.update(entity_id=entity_id,
                           values={field: [(5, )]},
                           options=options)

    @_ignore_none_errors
    def many_to_many_replace(self,
                             entity_id: int,
                             field: str,
                             related_ids: list[int],
                             options: dict[str, Any] = None,
                             ignore_none_errors: bool = False
                             ) -> bool:
        """
        Replace any existing related objects from a Many-to-Many relationship

        :param entity_id: The object ID from which remove the related object
        :param field: The field name for the relationship to update
        :param related_ids: List with the IDs of the records to replace
        :param options: Dictionary with options to use
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: True if the record was updated
        """
        return self.update(entity_id=entity_id,
                           values={field: [(6, 0, related_ids)]},
                           options=options)

    @_ignore_none_errors
    def execute(self,
                method_name: str,
                args: list[Any],
                kwargs: dict[str, Any],
                ignore_none_errors: bool = False
                ) -> Any:
        """
        Execute a method on a model

        :param method_name: The method name to call
        :param args: Arguments list passed by position
        :param kwargs: Arguments dict passed by keyword
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Method calling result data
        """
        return self.api.do_execute(method_name=method_name,
                                   args=args,
                                   kwargs=kwargs)

    @_ignore_none_errors
    def get_message_subtype_id(self,
                               subtype: str,
                               ignore_none_errors: bool = False
                               ) -> int:
        """
        Get Message subtype ID from its name

        :param subtype: Message subtype name
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Resulting ID
        """
        if subtype not in self._message_subtypes:
            item = self.get_model_data_reference(module_name='mail',
                                                 value=subtype)
            if item:
                self._message_subtypes[subtype] = item['res_id']
        return self._message_subtypes.get(subtype)

    @_ignore_none_errors
    def post_message(self,
                     subtype: Union[str, int],
                     entity_id: int,
                     author_id: int,
                     subject: Union[str, bool],
                     body: str,
                     options: Optional[dict[str, Any]] = None,
                     ignore_none_errors: bool = False
                     ) -> int:
        """
        Add a message to a model row

        :param subtype: Message subtype name or ID to post
        :param entity_id: The object ID to which to add the message
        :param author_id: The partner ID which authored the message
        :param subject: The message subject to add
        :param body: The message body to add
        :param options: Dictionary with any existing options
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: New message ID
        """
        subtype_id = (self.get_message_subtype_id(subtype)
                      if isinstance(subtype, str)
                      else subtype)
        return self.api.do_post_message(subtype_id=subtype_id,
                                        entity_id=entity_id,
                                        author_id=author_id,
                                        subject=subject,
                                        body=body,
                                        options=options)

    @_ignore_none_errors
    def post_message_as_activity(self,
                                 entity_id: int,
                                 body: str,
                                 author_id: int,
                                 ignore_none_errors: bool = False
                                 ) -> int:
        """
        Add an activity message to a model row

        :param entity_id: The object ID to which to add the message
        :param body: The message body to add
        :param author_id: The partner ID which authored the message
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Returned message ID
        """
        return self.post_message(subtype=MessageSubType.ACTIVITY,
                                 entity_id=entity_id,
                                 author_id=author_id,
                                 subject=False,
                                 body=body,
                                 options=None)

    @_ignore_none_errors
    def post_message_as_comment(self,
                                entity_id: int,
                                body: str,
                                author_id: int,
                                ignore_none_errors: bool = False
                                ) -> int:
        """
        Add a comment message to a model row

        :param entity_id: The object ID to which to add the message
        :param body: The message body to add
        :param author_id: The partner ID which authored the message
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Returned message ID
        """
        return self.post_message(subtype=MessageSubType.COMMENT,
                                 entity_id=entity_id,
                                 author_id=author_id,
                                 subject=False,
                                 body=body,
                                 options=None)

    @_ignore_none_errors
    def post_message_as_note(self,
                             entity_id: int,
                             body: str,
                             author_id: int,
                             ignore_none_errors: bool = False
                             ) -> int:
        """
        Add a note message to a model row

        :param entity_id: The object ID to which to add the message
        :param body: The message body to add
        :param author_id: The partner ID which authored the message
        :param ignore_none_errors: Ignore XML-RPC errors returning None
        :return: Returned message ID
        """
        return self.post_message(subtype=MessageSubType.NOTE,
                                 entity_id=entity_id,
                                 author_id=author_id,
                                 subject=False,
                                 body=body,
                                 options=None)
