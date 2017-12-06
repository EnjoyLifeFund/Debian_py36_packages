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


class SyncAgentKeyProperties(Model):
    """Properties of an Azure SQL Database sync agent key.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar sync_agent_key: Key of sync agent.
    :vartype sync_agent_key: str
    """

    _validation = {
        'sync_agent_key': {'readonly': True},
    }

    _attribute_map = {
        'sync_agent_key': {'key': 'syncAgentKey', 'type': 'str'},
    }

    def __init__(self):
        self.sync_agent_key = None
