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


class PoolUsageMetrics(Model):
    """Usage metrics for a pool across an aggregation interval.

    :param pool_id: The ID of the pool whose metrics are aggregated in this
     entry.
    :type pool_id: str
    :param start_time: The start time of the aggregation interval covered by
     this entry.
    :type start_time: datetime
    :param end_time: The end time of the aggregation interval covered by this
     entry.
    :type end_time: datetime
    :param vm_size: The size of virtual machines in the pool. All VMs in a
     pool are the same size. For information about available sizes of virtual
     machines for Cloud Services pools (pools created with
     cloudServiceConfiguration), see Sizes for Cloud Services
     (http://azure.microsoft.com/documentation/articles/cloud-services-sizes-specs/).
     Batch supports all Cloud Services VM sizes except ExtraSmall,
     STANDARD_A1_V2 and STANDARD_A2_V2. For information about available VM
     sizes for pools using images from the Virtual Machines Marketplace (pools
     created with virtualMachineConfiguration) see Sizes for Virtual Machines
     (Linux)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-linux-sizes/)
     or Sizes for Virtual Machines (Windows)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-windows-sizes/).
     Batch supports all Azure VM sizes except STANDARD_A0 and those with
     premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series).
    :type vm_size: str
    :param total_core_hours: The total core hours used in the pool during this
     aggregation interval.
    :type total_core_hours: float
    :param data_ingress_gi_b: The cross data center network ingress to the
     pool during this interval, in GiB.
    :type data_ingress_gi_b: float
    :param data_egress_gi_b: The cross data center network egress from the
     pool during this interval, in GiB.
    :type data_egress_gi_b: float
    """

    _validation = {
        'pool_id': {'required': True},
        'start_time': {'required': True},
        'end_time': {'required': True},
        'vm_size': {'required': True},
        'total_core_hours': {'required': True},
        'data_ingress_gi_b': {'required': True},
        'data_egress_gi_b': {'required': True},
    }

    _attribute_map = {
        'pool_id': {'key': 'poolId', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'vm_size': {'key': 'vmSize', 'type': 'str'},
        'total_core_hours': {'key': 'totalCoreHours', 'type': 'float'},
        'data_ingress_gi_b': {'key': 'dataIngressGiB', 'type': 'float'},
        'data_egress_gi_b': {'key': 'dataEgressGiB', 'type': 'float'},
    }

    def __init__(self, pool_id, start_time, end_time, vm_size, total_core_hours, data_ingress_gi_b, data_egress_gi_b):
        self.pool_id = pool_id
        self.start_time = start_time
        self.end_time = end_time
        self.vm_size = vm_size
        self.total_core_hours = total_core_hours
        self.data_ingress_gi_b = data_ingress_gi_b
        self.data_egress_gi_b = data_egress_gi_b
