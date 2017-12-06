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

from .health_evaluation import HealthEvaluation


class DeployedServicePackageHealthEvaluation(HealthEvaluation):
    """Represents health evaluation for a deployed service package, containing
    information about the data and the algorithm used by health store to
    evaluate health. The evaluation is returned only when the aggregated health
    state is either Error or Warning.

    :param aggregated_health_state: Possible values include: 'Invalid', 'Ok',
     'Warning', 'Error', 'Unknown'
    :type aggregated_health_state: str or :class:`enum
     <azure.servicefabric.models.enum>`
    :param description: Description of the health evaluation, which represents
     a summary of the evaluation process.
    :type description: str
    :param kind: Polymorphic Discriminator
    :type kind: str
    :param node_name:
    :type node_name: str
    :param application_name:
    :type application_name: str
    :param service_manifest_name:
    :type service_manifest_name: str
    :param unhealthy_evaluations:
    :type unhealthy_evaluations: list of :class:`HealthEvaluationWrapper
     <azure.servicefabric.models.HealthEvaluationWrapper>`
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'aggregated_health_state': {'key': 'AggregatedHealthState', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'node_name': {'key': 'NodeName', 'type': 'str'},
        'application_name': {'key': 'ApplicationName', 'type': 'str'},
        'service_manifest_name': {'key': 'ServiceManifestName', 'type': 'str'},
        'unhealthy_evaluations': {'key': 'UnhealthyEvaluations', 'type': '[HealthEvaluationWrapper]'},
    }

    def __init__(self, aggregated_health_state=None, description=None, node_name=None, application_name=None, service_manifest_name=None, unhealthy_evaluations=None):
        super(DeployedServicePackageHealthEvaluation, self).__init__(aggregated_health_state=aggregated_health_state, description=description)
        self.node_name = node_name
        self.application_name = application_name
        self.service_manifest_name = service_manifest_name
        self.unhealthy_evaluations = unhealthy_evaluations
        self.kind = 'DeployedServicePackage'