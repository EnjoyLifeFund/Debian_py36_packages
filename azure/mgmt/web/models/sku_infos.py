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


class SkuInfos(Model):
    """Collection of SKU information.

    :param resource_type: Resource type that this SKU applies to.
    :type resource_type: str
    :param skus: List of SKUs the subscription is able to use.
    :type skus: list[~azure.mgmt.web.models.GlobalCsmSkuDescription]
    """

    _attribute_map = {
        'resource_type': {'key': 'resourceType', 'type': 'str'},
        'skus': {'key': 'skus', 'type': '[GlobalCsmSkuDescription]'},
    }

    def __init__(self, resource_type=None, skus=None):
        self.resource_type = resource_type
        self.skus = skus
