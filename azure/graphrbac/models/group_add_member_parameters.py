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


class GroupAddMemberParameters(Model):
    """Request parameters for adding a member to a group.

    :param url: A member object URL, such as
     "https://graph.windows.net/0b1f9851-1bf0-433f-aec3-cb9272f093dc/directoryObjects/f260bbc4-c254-447b-94cf-293b5ec434dd",
     where "0b1f9851-1bf0-433f-aec3-cb9272f093dc" is the tenantId and
     "f260bbc4-c254-447b-94cf-293b5ec434dd" is the objectId of the member
     (user, application, servicePrincipal, group) to be added.
    :type url: str
    """

    _validation = {
        'url': {'required': True},
    }

    _attribute_map = {
        'url': {'key': 'url', 'type': 'str'},
    }

    def __init__(self, url):
        self.url = url