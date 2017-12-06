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


class JobStatus(Model):
    """JobStatus.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar execution_count: Gets the number of times this job has executed.
    :vartype execution_count: int
    :ivar failure_count: Gets the number of times this job has failed.
    :vartype failure_count: int
    :ivar faulted_count: Gets the number of faulted occurrences (occurrences
     that were retried and failed as many times as the retry policy states).
    :vartype faulted_count: int
    :ivar last_execution_time: Gets the time the last occurrence executed in
     ISO-8601 format.  Could be empty if job has not run yet.
    :vartype last_execution_time: datetime
    :ivar next_execution_time: Gets the time of the next occurrence in
     ISO-8601 format. Could be empty if the job is completed.
    :vartype next_execution_time: datetime
    """

    _validation = {
        'execution_count': {'readonly': True},
        'failure_count': {'readonly': True},
        'faulted_count': {'readonly': True},
        'last_execution_time': {'readonly': True},
        'next_execution_time': {'readonly': True},
    }

    _attribute_map = {
        'execution_count': {'key': 'executionCount', 'type': 'int'},
        'failure_count': {'key': 'failureCount', 'type': 'int'},
        'faulted_count': {'key': 'faultedCount', 'type': 'int'},
        'last_execution_time': {'key': 'lastExecutionTime', 'type': 'iso-8601'},
        'next_execution_time': {'key': 'nextExecutionTime', 'type': 'iso-8601'},
    }

    def __init__(self):
        self.execution_count = None
        self.failure_count = None
        self.faulted_count = None
        self.last_execution_time = None
        self.next_execution_time = None