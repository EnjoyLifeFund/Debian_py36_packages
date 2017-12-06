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


class JobExecutionInformation(Model):
    """Contains information about the execution of a job in the Azure Batch
    service.

    :param start_time: The start time of the job. This is the time at which
     the job was created.
    :type start_time: datetime
    :param end_time: The completion time of the job. This property is set only
     if the job is in the completed state.
    :type end_time: datetime
    :param pool_id: The ID of the pool to which this job is assigned. This
     element contains the actual pool where the job is assigned. When you get
     job details from the service, they also contain a poolInfo element, which
     contains the pool configuration data from when the job was added or
     updated. That poolInfo element may also contain a poolId element. If it
     does, the two IDs are the same. If it does not, it means the job ran on an
     auto pool, and this property contains the ID of that auto pool.
    :type pool_id: str
    :param scheduling_error: Details of any error encountered by the service
     in starting the job. This property is not set if there was no error
     starting the job.
    :type scheduling_error: :class:`JobSchedulingError
     <azure.batch.models.JobSchedulingError>`
    :param terminate_reason: A string describing the reason the job ended.
     This property is set only if the job is in the completed state. If the
     Batch service terminates the job, it sets the reason as follows:
     JMComplete - the Job Manager task completed, and killJobOnCompletion was
     set to true. MaxWallClockTimeExpiry - the job reached its maxWallClockTime
     constraint. TerminateJobSchedule - the job ran as part of a schedule, and
     the schedule terminated. AllTasksComplete - the job's onAllTasksComplete
     attribute is set to terminateJob, and all tasks in the job are complete.
     TaskFailed - the job's onTaskFailure attribute is set to
     performExitOptionsJobAction, and a task in the job failed with an exit
     condition that specified a jobAction of terminateJob. Any other string is
     a user-defined reason specified in a call to the 'Terminate a job'
     operation.
    :type terminate_reason: str
    """

    _validation = {
        'start_time': {'required': True},
    }

    _attribute_map = {
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'pool_id': {'key': 'poolId', 'type': 'str'},
        'scheduling_error': {'key': 'schedulingError', 'type': 'JobSchedulingError'},
        'terminate_reason': {'key': 'terminateReason', 'type': 'str'},
    }

    def __init__(self, start_time, end_time=None, pool_id=None, scheduling_error=None, terminate_reason=None):
        self.start_time = start_time
        self.end_time = end_time
        self.pool_id = pool_id
        self.scheduling_error = scheduling_error
        self.terminate_reason = terminate_reason