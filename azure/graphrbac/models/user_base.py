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

from msrest.serialization import Model


class UserBase(Model):
    """UserBase.

    :param immutable_id: This must be specified if you are using a federated
     domain for the user's userPrincipalName (UPN) property when creating a new
     user account. It is used to associate an on-premises Active Directory user
     account with their Azure AD user object.
    :type immutable_id: str
    :param usage_location: A two letter country code (ISO standard 3166).
     Required for users that will be assigned licenses due to legal requirement
     to check for availability of services in countries. Examples include:
     "US", "JP", and "GB".
    :type usage_location: str
    :param given_name: The given name for the user.
    :type given_name: str
    :param surname: The user's surname (family name or last name).
    :type surname: str
    :param user_type: A string value that can be used to classify user types
     in your directory, such as 'Member' and 'Guest'. Possible values include:
     'Member', 'Guest'
    :type user_type: str or ~azure.graphrbac.models.UserType
    """

    _attribute_map = {
        'immutable_id': {'key': 'immutableId', 'type': 'str'},
        'usage_location': {'key': 'usageLocation', 'type': 'str'},
        'given_name': {'key': 'givenName', 'type': 'str'},
        'surname': {'key': 'surname', 'type': 'str'},
        'user_type': {'key': 'userType', 'type': 'str'},
    }

    def __init__(self, immutable_id=None, usage_location=None, given_name=None, surname=None, user_type=None):
        self.immutable_id = immutable_id
        self.usage_location = usage_location
        self.given_name = given_name
        self.surname = surname
        self.user_type = user_type
