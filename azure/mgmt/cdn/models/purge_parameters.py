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


class PurgeParameters(Model):
    """Parameters required for content purge.

    :param content_paths: The path to the content to be purged. Can describe a
     file path or a wild card directory.
    :type content_paths: list[str]
    """

    _validation = {
        'content_paths': {'required': True},
    }

    _attribute_map = {
        'content_paths': {'key': 'contentPaths', 'type': '[str]'},
    }

    def __init__(self, content_paths):
        self.content_paths = content_paths