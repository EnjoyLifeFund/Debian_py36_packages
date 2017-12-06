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

from .sub_resource import SubResource


class WorkflowTrigger(SubResource):
    """The workflow trigger.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The resource id.
    :vartype id: str
    :ivar provisioning_state: Gets the provisioning state. Possible values
     include: 'NotSpecified', 'Accepted', 'Running', 'Ready', 'Creating',
     'Created', 'Deleting', 'Deleted', 'Canceled', 'Failed', 'Succeeded',
     'Moving', 'Updating', 'Registering', 'Registered', 'Unregistering',
     'Unregistered', 'Completed'
    :vartype provisioning_state: str or
     :class:`WorkflowTriggerProvisioningState
     <azure.mgmt.logic.models.WorkflowTriggerProvisioningState>`
    :ivar created_time: Gets the created time.
    :vartype created_time: datetime
    :ivar changed_time: Gets the changed time.
    :vartype changed_time: datetime
    :ivar state: Gets the state. Possible values include: 'NotSpecified',
     'Completed', 'Enabled', 'Disabled', 'Deleted', 'Suspended'
    :vartype state: str or :class:`WorkflowState
     <azure.mgmt.logic.models.WorkflowState>`
    :ivar status: Gets the status. Possible values include: 'NotSpecified',
     'Paused', 'Running', 'Waiting', 'Succeeded', 'Skipped', 'Suspended',
     'Cancelled', 'Failed', 'Faulted', 'TimedOut', 'Aborted', 'Ignored'
    :vartype status: str or :class:`WorkflowStatus
     <azure.mgmt.logic.models.WorkflowStatus>`
    :ivar last_execution_time: Gets the last execution time.
    :vartype last_execution_time: datetime
    :ivar next_execution_time: Gets the next execution time.
    :vartype next_execution_time: datetime
    :ivar recurrence: Gets the workflow trigger recurrence.
    :vartype recurrence: :class:`WorkflowTriggerRecurrence
     <azure.mgmt.logic.models.WorkflowTriggerRecurrence>`
    :ivar workflow: Gets the reference to workflow.
    :vartype workflow: :class:`ResourceReference
     <azure.mgmt.logic.models.ResourceReference>`
    :ivar name: Gets the workflow trigger name.
    :vartype name: str
    :ivar type: Gets the workflow trigger type.
    :vartype type: str
    """

    _validation = {
        'id': {'readonly': True},
        'provisioning_state': {'readonly': True},
        'created_time': {'readonly': True},
        'changed_time': {'readonly': True},
        'state': {'readonly': True},
        'status': {'readonly': True},
        'last_execution_time': {'readonly': True},
        'next_execution_time': {'readonly': True},
        'recurrence': {'readonly': True},
        'workflow': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'WorkflowTriggerProvisioningState'},
        'created_time': {'key': 'properties.createdTime', 'type': 'iso-8601'},
        'changed_time': {'key': 'properties.changedTime', 'type': 'iso-8601'},
        'state': {'key': 'properties.state', 'type': 'WorkflowState'},
        'status': {'key': 'properties.status', 'type': 'WorkflowStatus'},
        'last_execution_time': {'key': 'properties.lastExecutionTime', 'type': 'iso-8601'},
        'next_execution_time': {'key': 'properties.nextExecutionTime', 'type': 'iso-8601'},
        'recurrence': {'key': 'properties.recurrence', 'type': 'WorkflowTriggerRecurrence'},
        'workflow': {'key': 'properties.workflow', 'type': 'ResourceReference'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self):
        super(WorkflowTrigger, self).__init__()
        self.provisioning_state = None
        self.created_time = None
        self.changed_time = None
        self.state = None
        self.status = None
        self.last_execution_time = None
        self.next_execution_time = None
        self.recurrence = None
        self.workflow = None
        self.name = None
        self.type = None
