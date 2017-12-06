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


class IpAddressGroup(Model):
    """CDN Ip address group.

    :param delivery_region: The delivery region of the ip address group
    :type delivery_region: str
    :param ipv4_addresses: The list of ip v4 addresses.
    :type ipv4_addresses: list[~azure.mgmt.cdn.models.CidrIpAddress]
    :param ipv6_addresses: The list of ip v6 addresses.
    :type ipv6_addresses: list[~azure.mgmt.cdn.models.CidrIpAddress]
    """

    _attribute_map = {
        'delivery_region': {'key': 'deliveryRegion', 'type': 'str'},
        'ipv4_addresses': {'key': 'ipv4Addresses', 'type': '[CidrIpAddress]'},
        'ipv6_addresses': {'key': 'ipv6Addresses', 'type': '[CidrIpAddress]'},
    }

    def __init__(self, delivery_region=None, ipv4_addresses=None, ipv6_addresses=None):
        self.delivery_region = delivery_region
        self.ipv4_addresses = ipv4_addresses
        self.ipv6_addresses = ipv6_addresses