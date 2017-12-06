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


class EntityHealthStateChunk(Model):
    """A base type for the health state chunk of various entities in the cluster.
    It contains the aggregated health state.

    :param health_state: Possible values include: 'Invalid', 'Ok', 'Warning',
     'Error', 'Unknown'
    :type health_state: str or :class:`enum <azure.servicefabric.models.enum>`
    """

    _attribute_map = {
        'health_state': {'key': 'HealthState', 'type': 'str'},
    }

    def __init__(self, health_state=None):
        self.health_state = health_state
