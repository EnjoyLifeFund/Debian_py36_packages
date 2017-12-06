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


class TrafficManagerNameAvailability(Model):
    """Class representing a Traffic Manager Name Availability response.

    :param name: The relative name.
    :type name: str
    :param type: Traffic Manager profile resource type.
    :type type: str
    :param name_available: Describes whether the relative name is available or
     not.
    :type name_available: bool
    :param reason: The reason why the name is not available, when applicable.
    :type reason: str
    :param message: Descriptive message that explains why the name is not
     available, when applicable.
    :type message: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'name_available': {'key': 'nameAvailable', 'type': 'bool'},
        'reason': {'key': 'reason', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
    }

    def __init__(self, name=None, type=None, name_available=None, reason=None, message=None):
        self.name = name
        self.type = type
        self.name_available = name_available
        self.reason = reason
        self.message = message
