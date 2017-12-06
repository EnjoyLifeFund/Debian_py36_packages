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


class Contact(Model):
    """Contact information for domain registration. If 'Domain Privacy' option is
    not selected then the contact information is made publicly available
    through the Whois
    directories as per ICANN requirements.

    :param address_mailing: Mailing address.
    :type address_mailing: ~azure.mgmt.web.models.Address
    :param email: Email address.
    :type email: str
    :param fax: Fax number.
    :type fax: str
    :param job_title: Job title.
    :type job_title: str
    :param name_first: First name.
    :type name_first: str
    :param name_last: Last name.
    :type name_last: str
    :param name_middle: Middle name.
    :type name_middle: str
    :param organization: Organization.
    :type organization: str
    :param phone: Phone number.
    :type phone: str
    """

    _validation = {
        'email': {'required': True},
        'name_first': {'required': True},
        'name_last': {'required': True},
        'phone': {'required': True},
    }

    _attribute_map = {
        'address_mailing': {'key': 'addressMailing', 'type': 'Address'},
        'email': {'key': 'email', 'type': 'str'},
        'fax': {'key': 'fax', 'type': 'str'},
        'job_title': {'key': 'jobTitle', 'type': 'str'},
        'name_first': {'key': 'nameFirst', 'type': 'str'},
        'name_last': {'key': 'nameLast', 'type': 'str'},
        'name_middle': {'key': 'nameMiddle', 'type': 'str'},
        'organization': {'key': 'organization', 'type': 'str'},
        'phone': {'key': 'phone', 'type': 'str'},
    }

    def __init__(self, email, name_first, name_last, phone, address_mailing=None, fax=None, job_title=None, name_middle=None, organization=None):
        self.address_mailing = address_mailing
        self.email = email
        self.fax = fax
        self.job_title = job_title
        self.name_first = name_first
        self.name_last = name_last
        self.name_middle = name_middle
        self.organization = organization
        self.phone = phone