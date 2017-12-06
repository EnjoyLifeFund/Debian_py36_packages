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

from .proxy_resource import ProxyResource


class FailoverGroup(ProxyResource):
    """A failover group.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Resource ID.
    :vartype id: str
    :ivar name: Resource name.
    :vartype name: str
    :ivar type: Resource type.
    :vartype type: str
    :ivar location: Resource location.
    :vartype location: str
    :param tags: Resource tags.
    :type tags: dict[str, str]
    :param read_write_endpoint: Read-write endpoint of the failover group
     instance.
    :type read_write_endpoint:
     ~azure.mgmt.sql.models.FailoverGroupReadWriteEndpoint
    :param read_only_endpoint: Read-only endpoint of the failover group
     instance.
    :type read_only_endpoint:
     ~azure.mgmt.sql.models.FailoverGroupReadOnlyEndpoint
    :ivar replication_role: Local replication role of the failover group
     instance. Possible values include: 'Primary', 'Secondary'
    :vartype replication_role: str or
     ~azure.mgmt.sql.models.FailoverGroupReplicationRole
    :ivar replication_state: Replication state of the failover group instance.
    :vartype replication_state: str
    :param partner_servers: List of partner server information for the
     failover group.
    :type partner_servers: list[~azure.mgmt.sql.models.PartnerInfo]
    :param databases: List of databases in the failover group.
    :type databases: list[str]
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'location': {'readonly': True},
        'read_write_endpoint': {'required': True},
        'replication_role': {'readonly': True},
        'replication_state': {'readonly': True},
        'partner_servers': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'read_write_endpoint': {'key': 'properties.readWriteEndpoint', 'type': 'FailoverGroupReadWriteEndpoint'},
        'read_only_endpoint': {'key': 'properties.readOnlyEndpoint', 'type': 'FailoverGroupReadOnlyEndpoint'},
        'replication_role': {'key': 'properties.replicationRole', 'type': 'str'},
        'replication_state': {'key': 'properties.replicationState', 'type': 'str'},
        'partner_servers': {'key': 'properties.partnerServers', 'type': '[PartnerInfo]'},
        'databases': {'key': 'properties.databases', 'type': '[str]'},
    }

    def __init__(self, read_write_endpoint, partner_servers, tags=None, read_only_endpoint=None, databases=None):
        super(FailoverGroup, self).__init__()
        self.location = None
        self.tags = tags
        self.read_write_endpoint = read_write_endpoint
        self.read_only_endpoint = read_only_endpoint
        self.replication_role = None
        self.replication_state = None
        self.partner_servers = partner_servers
        self.databases = databases