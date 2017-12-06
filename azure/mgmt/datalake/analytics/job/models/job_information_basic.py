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


class JobInformationBasic(Model):
    """The common Data Lake Analytics job information properties.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar job_id: the job's unique identifier (a GUID).
    :vartype job_id: str
    :param name: the friendly name of the job.
    :type name: str
    :param type: the job type of the current job (Hive or USql). Possible
     values include: 'USql', 'Hive'
    :type type: str or :class:`JobType
     <azure.mgmt.datalake.analytics.job.models.JobType>`
    :ivar submitter: the user or account that submitted the job.
    :vartype submitter: str
    :param degree_of_parallelism: the degree of parallelism used for this job.
     This must be greater than 0, if set to less than 0 it will default to 1.
     Default value: 1 .
    :type degree_of_parallelism: int
    :param priority: the priority value for the current job. Lower numbers
     have a higher priority. By default, a job has a priority of 1000. This
     must be greater than 0.
    :type priority: int
    :ivar submit_time: the time the job was submitted to the service.
    :vartype submit_time: datetime
    :ivar start_time: the start time of the job.
    :vartype start_time: datetime
    :ivar end_time: the completion time of the job.
    :vartype end_time: datetime
    :ivar state: the job state. When the job is in the Ended state, refer to
     Result and ErrorMessage for details. Possible values include: 'Accepted',
     'Compiling', 'Ended', 'New', 'Queued', 'Running', 'Scheduling',
     'Starting', 'Paused', 'WaitingForCapacity'
    :vartype state: str or :class:`JobState
     <azure.mgmt.datalake.analytics.job.models.JobState>`
    :ivar result: the result of job execution or the current result of the
     running job. Possible values include: 'None', 'Succeeded', 'Cancelled',
     'Failed'
    :vartype result: str or :class:`JobResult
     <azure.mgmt.datalake.analytics.job.models.JobResult>`
    :ivar log_folder: the log folder path to use in the following format:
     adl://<accountName>.azuredatalakestore.net/system/jobservice/jobs/Usql/2016/03/13/17/18/5fe51957-93bc-4de0-8ddc-c5a4753b068b/logs/.
    :vartype log_folder: str
    :param log_file_patterns: the list of log file name patterns to find in
     the logFolder. '*' is the only matching character allowed. Example format:
     jobExecution*.log or *mylog*.txt
    :type log_file_patterns: list of str
    :param related: the recurring job relationship information properties.
    :type related: :class:`JobRelationshipProperties
     <azure.mgmt.datalake.analytics.job.models.JobRelationshipProperties>`
    """

    _validation = {
        'job_id': {'readonly': True},
        'name': {'required': True},
        'type': {'required': True},
        'submitter': {'readonly': True},
        'submit_time': {'readonly': True},
        'start_time': {'readonly': True},
        'end_time': {'readonly': True},
        'state': {'readonly': True},
        'result': {'readonly': True},
        'log_folder': {'readonly': True},
    }

    _attribute_map = {
        'job_id': {'key': 'jobId', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'JobType'},
        'submitter': {'key': 'submitter', 'type': 'str'},
        'degree_of_parallelism': {'key': 'degreeOfParallelism', 'type': 'int'},
        'priority': {'key': 'priority', 'type': 'int'},
        'submit_time': {'key': 'submitTime', 'type': 'iso-8601'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'state': {'key': 'state', 'type': 'JobState'},
        'result': {'key': 'result', 'type': 'JobResult'},
        'log_folder': {'key': 'logFolder', 'type': 'str'},
        'log_file_patterns': {'key': 'logFilePatterns', 'type': '[str]'},
        'related': {'key': 'related', 'type': 'JobRelationshipProperties'},
    }

    def __init__(self, name, type, degree_of_parallelism=1, priority=None, log_file_patterns=None, related=None):
        self.job_id = None
        self.name = name
        self.type = type
        self.submitter = None
        self.degree_of_parallelism = degree_of_parallelism
        self.priority = priority
        self.submit_time = None
        self.start_time = None
        self.end_time = None
        self.state = None
        self.result = None
        self.log_folder = None
        self.log_file_patterns = log_file_patterns
        self.related = related
