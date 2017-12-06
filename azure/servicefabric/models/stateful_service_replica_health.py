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

from .replica_health import ReplicaHealth


class StatefulServiceReplicaHealth(ReplicaHealth):
    """Represents the health of the stateful service replica.
    Contains the replica aggregated health state, the health events and the
    unhealthy evaluations.
    .

    :param aggregated_health_state: Possible values include: 'Invalid', 'Ok',
     'Warning', 'Error', 'Unknown'
    :type aggregated_health_state: str or :class:`enum
     <azure.servicefabric.models.enum>`
    :param health_events: The list of health events reported on the entity.
    :type health_events: list of :class:`HealthEvent
     <azure.servicefabric.models.HealthEvent>`
    :param unhealthy_evaluations:
    :type unhealthy_evaluations: list of :class:`HealthEvaluationWrapper
     <azure.servicefabric.models.HealthEvaluationWrapper>`
    :param health_statistics:
    :type health_statistics: :class:`HealthStatistics
     <azure.servicefabric.models.HealthStatistics>`
    :param partition_id:
    :type partition_id: str
    :param service_kind: Polymorphic Discriminator
    :type service_kind: str
    :param replica_id:
    :type replica_id: str
    """

    _validation = {
        'service_kind': {'required': True},
    }

    _attribute_map = {
        'aggregated_health_state': {'key': 'AggregatedHealthState', 'type': 'str'},
        'health_events': {'key': 'HealthEvents', 'type': '[HealthEvent]'},
        'unhealthy_evaluations': {'key': 'UnhealthyEvaluations', 'type': '[HealthEvaluationWrapper]'},
        'health_statistics': {'key': 'HealthStatistics', 'type': 'HealthStatistics'},
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
        'service_kind': {'key': 'ServiceKind', 'type': 'str'},
        'replica_id': {'key': 'ReplicaId', 'type': 'str'},
    }

    def __init__(self, aggregated_health_state=None, health_events=None, unhealthy_evaluations=None, health_statistics=None, partition_id=None, replica_id=None):
        super(StatefulServiceReplicaHealth, self).__init__(aggregated_health_state=aggregated_health_state, health_events=health_events, unhealthy_evaluations=unhealthy_evaluations, health_statistics=health_statistics, partition_id=partition_id)
        self.replica_id = replica_id
        self.service_kind = 'Stateful'