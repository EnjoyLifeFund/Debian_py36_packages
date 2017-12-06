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


class NodeUpgradeProgressInfo(Model):
    """Information about the upgrading node and its status.

    :param node_name:
    :type node_name: str
    :param upgrade_phase: Possible values include: 'Invalid',
     'PreUpgradeSafetyCheck', 'Upgrading', 'PostUpgradeSafetyCheck'
    :type upgrade_phase: str or :class:`enum
     <azure.servicefabric.models.enum>`
    :param pending_safety_checks:
    :type pending_safety_checks: list of :class:`SafetyCheckWrapper
     <azure.servicefabric.models.SafetyCheckWrapper>`
    """

    _attribute_map = {
        'node_name': {'key': 'NodeName', 'type': 'str'},
        'upgrade_phase': {'key': 'UpgradePhase', 'type': 'str'},
        'pending_safety_checks': {'key': 'PendingSafetyChecks', 'type': '[SafetyCheckWrapper]'},
    }

    def __init__(self, node_name=None, upgrade_phase=None, pending_safety_checks=None):
        self.node_name = node_name
        self.upgrade_phase = upgrade_phase
        self.pending_safety_checks = pending_safety_checks