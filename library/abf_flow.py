#!/usr/bin/python

# TODO: Add copyright data here
#
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: abf_flow
short_description: Create new Application Flows on Algosec Business Flow.
description:
    - If the requested flow is a subset of one of the flows of the relevant Application, flow creation is cancelled.
version_added: null
author: "Almog Cohen (@AlmogCohen)"
options:
    ip_address:
        required: true
        description:
            - IP address (or hostname) of the Algosec server.
    user:
        required: true
        description:
            - Username credentials to use for auth.
    password:
        required: true
        description:
            - Password credentials to use for auth.
    app_name:
        required: true
        description:
            - BusinessFlow Application to add the flow to.
    name:
        required: false
        description:
            - Name for the flow to be created
    sources:
        required: true
        description:
            - Comma separated IP list of traffic sources for the flow
    destinations:
        required: true
        description:
            - Comma separated IP list of traffic destinations for the flow
    services:
        required: true
        description:
            - Comma separated list of traffic services to allow in the flow. Services can be as defined on Algosec
            - BusinessFlow or in a proto/port format (only UDP and TCP are supported as proto. e.g. tcp/50).
    users:
        default: []
        description:
            - Comma separated list of users the flow is relevant to.
    network_applications:
        default: []
        description:
            - Comma separated list of network application names the flow is relevant to.
    comment:
        default: Flow created by AlgosecAnsible
        description:
            - Comment to attach to the flow

requirements:
    - algosec~=0.2.0 (can be obtained from PyPi https://pypi.python.org/pypi/algosec)
"""

EXAMPLES = """
   - name: Create a flow on an AlsogsecBusinessFlow App
     hosts: algosec-server

     tasks:
     - name: Create the flow on ABF
       # We use delegation to use the local python interpreter (and virtualenv if enabled)
       delegate_to: localhost
       abf_flow:
         ip_address: 192.168.58.128
         user: admin
         password: S0mePA$$w0rd

         app_name: Payroll
         name: payroll-server-auth
         sources: 192.168.12.12
         destinations: 16.47.71.62,16.47.71.63
         services: HTTPS,tcp/23
"""

RETURN = """
changed:
    description: 
    returned:
        - always
    type: bool
    sample: True, False
"""

import traceback
from ansible.module_utils.basic import AnsibleModule


try:
    from algosec.api_client import AlgosecBusinessFlowAPIClient
    from algosec.errors import AlgosecAPIError
    from algosec.models import RequestedFlow
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    module = AnsibleModule(
        # TODO: Support the check mode actually within the module
        supports_check_mode=True,
        argument_spec=dict(
            # arguments used for creating the flow
            ip_address=dict(required=True),
            user=dict(required=True, aliases=['username']),
            password=dict(aliases=['pass', 'pwd'], required=True, no_log=True),
            app_name=dict(required=True),
            name=dict(required=False),
            sources=dict(type='list', required=True),
            destinations=dict(type='list', required=True),
            services=dict(type='list', required=True),
            users=dict(type='list', required=False, default=[]),
            network_applications=dict(type='list', required=False, default=[]),
            comment=dict(required=False, default="Flow created by AlgosecAnsible"),
            # custom_fields=dict(type='str', required=False),
        ),
    )

    if not HAS_LIB:
        module.fail_json(msg='algoec package is required for this module')

    app_name = module.params["app_name"]
    flow_name = module.params["name"]
    try:
        api = AlgosecBusinessFlowAPIClient(
            module.params["ip_address"],
            module.params["user"],
            module.params["password"],
        )
        app_id = api.get_application_id_by_name(app_name)

        requested_flow = RequestedFlow(
            name=flow_name,
            sources=module.params["sources"],
            destinations=module.params["destinations"],
            network_users=module.params["users"],
            network_applications=module.params["network_applications"],
            network_services=module.params["services"],
            comment=module.params["comment"],
        )
        requested_flow.populate(api)

        if api.does_flow_exist(app_id, requested_flow):
            changed = False
        else:
            api.create_application_flow(app_id, requested_flow)
            # to finalize the application flow creation, The application's draft version is applied
            api.apply_application_draft(app_id)
            changed = True

        module.exit_json(changed=changed, msg="Done!")

    except AlgosecAPIError:
        module.fail_json(msg=(traceback.format_exc()))


if __name__ == '__main__':
    main()
