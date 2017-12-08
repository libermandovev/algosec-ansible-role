#!/usr/bin/python

# TODO: Add copyright data here
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: aff
short_description: Check and create traffic change requests with Algosec FireFlow.
description:
    - Algosec Ansible module will help you manage and orchestrate your tasks to work with Algosec FireFlow service.
    - When used, the `aff` command will check if a certain traffic is allowed between `source` and `dest`.
    - If the connectivity is not allowed between the nodes, the module will create a "Change Request"
    - on Algosec's FireFlow and will provide the change request url in the module call result.
author: "Almog Cohen (@AlmogCohen)"

requirements:
    - algosec - python package that should be obtained internally
    
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
    requestor:
        required: true
        description:
            - The first and last name of the requester.
    email:
        required: true
        description:
            - The email address of the requester.
    sources:
        required: true
        description:
            - Comma separated list of IP address for the traffic sources.
            - For example: 192.168.1.5, PAYROLL_WEB_SERVER
    destinations:
        required: true
        description:
            - Comma separated list of IP address for the traffic destinations.
            - For example: 192.168.1.5, PAYROLL_WEB_SERVER
    services:
        required: true
        description:
            - List of services of the traffic to allow. Accepted services are as defined on Algosec or by port/proto format
               (e.g. tcp/50,udp/100,ssh).
    transport:
        default: ipv4
        choices: [ ipv4, ipv6 ]
        description:
            - Set the network connectivity check transport layer type.

"""

EXAMPLES = """
- hosts: localhost
  connection: local
  tasks:
      - name: Create the FireFlow ticket if traffic not allowed
       aff_allow_traffic:
          ip_address: "{{ ip_address }}"
          user: "{{ username }}"
          password: "{{ password }}"
          
          # Specific connectivity check parameters
          requestor: almogco
          email: almog@algosec.com
          sources: 192.168.1.1,192.168.1.2
          destinations: 8.8.8.8,4.4.4.4
          services: http,dns
       register: result
- name: Display the url for the created change request ticket (if already registered)
    - debug: var=result
"""

RETURN = """
is_traffic_allowed:
    description: State whether the traffic is currently allowed
    returned:
        - always
    type: bool
    sample: True, False
connectivity_status:
    description: The current connectivity status of the traffic. Can be Allowed, Blocked, Partially Blocked or Not Routed.
    returned:
        - always
    type: string
    sample: Partially, Allowed, Blocked, Not Routed
change_request_url:
    description: URL for the change request ticket on the Algosec server
    returned:
        - on traffic Change Request creation
    type: string
    sample: https://192.168.58.128/FireFlow/Ticket/Display.html?id=2410
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception

try:
    from algosec.api_client import AlgosecFirewallAnalyzerAPIClient, AlgosecFireFlowAPIClient
    from algosec.errors import AlgosecAPIError
    from algosec.models import DeviceAllowanceState, ChangeRequestAction

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            ip_address=dict(required=True),
            user=dict(required=True, aliases=['username']),
            password=dict(aliases=['pass', 'pwd'], required=True, no_log=True),
            requester=dict(required=True),
            email=dict(required=True),
            # action=dict(default='allow', choices=['allow', 'drop']),
            sources=dict(type='list', required=True),
            destinations=dict(type='list', required=True),
            services=dict(type='list', required=True),
            transport=dict(default='ipv4', required=False, choices=['ipv4', 'ipv6'])
        )
    )

    if not HAS_LIB:
        module.fail_json(msg='algoec package is required for this module')

    try:
        afa_client = AlgosecFirewallAnalyzerAPIClient(
            module.params["ip_address"],
            module.params["user"],
            module.params["password"],
        )
        connectivity_status = afa_client.check_connectivity_status(
            source=module.params['sources'],
            dest=module.params['destinations'],
            service=module.params['services'],
        )
    except AlgosecAPIError:
        exc = get_exception()
        module.fail_json(msg="Error executing traffic simulation:\n{}".format(exc.message))
        return

    response = {'connectivity_status': connectivity_status.value.text}
    if connectivity_status == DeviceAllowanceState.ALLOWED:
        module.log('Connectivity check passed. No FireFlow ticket is required')
        response['is_traffic_allowed'] = True
        response['changed'] = False
    else:
        response['is_traffic_allowed'] = False

        module.log(
            'Connectivity status is {}. Opening ticket on Algosec FireFlow at {}'.format(
                connectivity_status,
                module.params['algosec_host']
            )
        )
        if not module.check_mode:
            try:
                aff_client = AlgosecFireFlowAPIClient(
                    module.params["ip_address"],
                    module.params["user"],
                    module.params["password"],
                )
                requester = module.params['requester']
                change_request_url = aff_client.create_change_request(
                    # TODO: drop action is not yet supported
                    action=ChangeRequestAction.ALLOW,
                    subject="Allow {} traffic from {} to {} (issued via Ansible)".format(
                        module.params['services'],
                        module.params['sources'],
                        module.params['destinations']
                    ),
                    requester_name=requester,
                    email=module.params['email'],
                    sources=module.params['sources'],
                    destinations=module.params['destinations'],
                    services=module.params['services'],
                    description="Traffic change request created by {} directly from Ansible.".format(requester)
                )
            except AlgosecAPIError:
                exc = get_exception()
                module.fail_json(msg="Error creating change request:\n{}".format(exc.message))
                return
            response['change_request_url'] = change_request_url
        response['changed'] = True

    module.exit_json(**response)


if __name__ == '__main__':
    main()
