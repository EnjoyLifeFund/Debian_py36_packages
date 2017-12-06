# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

import uuid
from msrest.pipeline import ClientRawResponse

from .. import models


class UsersOperations(object):
    """UsersOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :ivar api_version: Client API version. Constant value: "1.6".
    """

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "1.6"

        self.config = config

    def create(
            self, parameters, custom_headers=None, raw=False, **operation_config):
        """Create a new user.

        :param parameters: Parameters to create a user.
        :type parameters: ~azure.graphrbac.models.UserCreateParameters
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: User or ClientRawResponse if raw=true
        :rtype: ~azure.graphrbac.models.User or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        # Construct URL
        url = '/{tenantID}/users'
        path_format_arguments = {
            'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(parameters, 'UserCreateParameters')

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, **operation_config)

        if response.status_code not in [201]:
            raise models.GraphErrorException(self._deserialize, response)

        deserialized = None

        if response.status_code == 201:
            deserialized = self._deserialize('User', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    def list(
            self, filter=None, custom_headers=None, raw=False, **operation_config):
        """Gets list of users for the current tenant.

        :param filter: The filter to apply to the operation.
        :type filter: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: An iterator like instance of User
        :rtype:
         ~azure.graphrbac.models.UserPaged[~azure.graphrbac.models.User]
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        def internal_paging(next_link=None, raw=False):

            if not next_link:
                # Construct URL
                url = '/{tenantID}/users'
                path_format_arguments = {
                    'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
                }
                url = self._client.format_url(url, **path_format_arguments)

                # Construct parameters
                query_parameters = {}
                if filter is not None:
                    query_parameters['$filter'] = self._serialize.query("filter", filter, 'str')
                query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

            else:
                url = '/{tenantID}/{nextLink}'
                path_format_arguments = {
                    'nextLink': self._serialize.url("next_link", next_link, 'str', skip_quote=True),
                    'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
                }
                url = self._client.format_url(url, **path_format_arguments)
                query_parameters = {}
                query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

            # Construct headers
            header_parameters = {}
            header_parameters['Content-Type'] = 'application/json; charset=utf-8'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

            # Construct and send request
            request = self._client.get(url, query_parameters)
            response = self._client.send(
                request, header_parameters, **operation_config)

            if response.status_code not in [200]:
                raise models.GraphErrorException(self._deserialize, response)

            return response

        # Deserialize response
        deserialized = models.UserPaged(internal_paging, self._deserialize.dependencies)

        if raw:
            header_dict = {}
            client_raw_response = models.UserPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response

        return deserialized

    def get(
            self, upn_or_object_id, custom_headers=None, raw=False, **operation_config):
        """Gets user information from the directory.

        :param upn_or_object_id: The object ID or principal name of the user
         for which to get information.
        :type upn_or_object_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: User or ClientRawResponse if raw=true
        :rtype: ~azure.graphrbac.models.User or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        # Construct URL
        url = '/{tenantID}/users/{upnOrObjectId}'
        path_format_arguments = {
            'upnOrObjectId': self._serialize.url("upn_or_object_id", upn_or_object_id, 'str'),
            'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)

        if response.status_code not in [200]:
            raise models.GraphErrorException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('User', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    def update(
            self, upn_or_object_id, parameters, custom_headers=None, raw=False, **operation_config):
        """Updates a user.

        :param upn_or_object_id: The object ID or principal name of the user
         to update.
        :type upn_or_object_id: str
        :param parameters: Parameters to update an existing user.
        :type parameters: ~azure.graphrbac.models.UserUpdateParameters
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        # Construct URL
        url = '/{tenantID}/users/{upnOrObjectId}'
        path_format_arguments = {
            'upnOrObjectId': self._serialize.url("upn_or_object_id", upn_or_object_id, 'str'),
            'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(parameters, 'UserUpdateParameters')

        # Construct and send request
        request = self._client.patch(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, **operation_config)

        if response.status_code not in [204]:
            raise models.GraphErrorException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response

    def delete(
            self, upn_or_object_id, custom_headers=None, raw=False, **operation_config):
        """Delete a user.

        :param upn_or_object_id: The object ID or principal name of the user
         to delete.
        :type upn_or_object_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        # Construct URL
        url = '/{tenantID}/users/{upnOrObjectId}'
        path_format_arguments = {
            'upnOrObjectId': self._serialize.url("upn_or_object_id", upn_or_object_id, 'str'),
            'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)

        if response.status_code not in [204]:
            raise models.GraphErrorException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response

    def get_member_groups(
            self, object_id, security_enabled_only, custom_headers=None, raw=False, **operation_config):
        """Gets a collection that contains the object IDs of the groups of which
        the user is a member.

        :param object_id: The object ID of the user for which to get group
         membership.
        :type object_id: str
        :param security_enabled_only: If true, only membership in
         security-enabled groups should be checked. Otherwise, membership in
         all groups should be checked.
        :type security_enabled_only: bool
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: An iterator like instance of str
        :rtype: ~azure.graphrbac.models.StrPaged[str]
        :raises:
         :class:`GraphErrorException<azure.graphrbac.models.GraphErrorException>`
        """
        parameters = models.UserGetMemberGroupsParameters(security_enabled_only=security_enabled_only)

        def internal_paging(next_link=None, raw=False):

            if not next_link:
                # Construct URL
                url = '/{tenantID}/users/{objectId}/getMemberGroups'
                path_format_arguments = {
                    'objectId': self._serialize.url("object_id", object_id, 'str'),
                    'tenantID': self._serialize.url("self.config.tenant_id", self.config.tenant_id, 'str')
                }
                url = self._client.format_url(url, **path_format_arguments)

                # Construct parameters
                query_parameters = {}
                query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

            else:
                url = next_link
                query_parameters = {}

            # Construct headers
            header_parameters = {}
            header_parameters['Content-Type'] = 'application/json; charset=utf-8'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

            # Construct body
            body_content = self._serialize.body(parameters, 'UserGetMemberGroupsParameters')

            # Construct and send request
            request = self._client.post(url, query_parameters)
            response = self._client.send(
                request, header_parameters, body_content, **operation_config)

            if response.status_code not in [200]:
                raise models.GraphErrorException(self._deserialize, response)

            return response

        # Deserialize response
        deserialized = models.StrPaged(internal_paging, self._deserialize.dependencies)

        if raw:
            header_dict = {}
            client_raw_response = models.StrPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response

        return deserialized
