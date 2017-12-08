#!/usr/bin/python

# TODO: Add copyright data here
#
# ANSIBLE_METADATA = {
#     'metadata_version': '1.0',
#     'status': ['preview'],
#     'supported_by': 'community'
# }
#
# DOCUMENTATION = """
# ---
# module: aff
# short_description: Check and create traffic change requests with Algosec FireFlow.
# description:
#     - Algosec Ansible module will help you manage and orchestrate your tasks to work with Algosec FireFlow server.
#     - When used, the `aff` command will check if a certain traffic is allowed between `source` and `dest`.
#     - If the connectivity is not allowed between the nodes, the module will create a "Change Request"
#     - on Algosec's FireFlow and will provide the change request url in the module call result.
# version_added: null
# author: "Almog Cohen (@AlmogCohen)"
# options:
#     algosec_host:
#         required: true
#         description:
#             - Hostname of your accesible Algosec's server (e.g. 192.168.12.200, algosec.internal).
#     user:
#         required: true
#         description:
#             - The username that will be used to sign-in into Algosec's server and create the Traffic Change Request.
#     password:
#         required: true
#         description:
#             - The password that will be used to sign-in into Algosec's server and create the Traffic Change Request.
#     requestor:
#         required: true
#         description:
#             - The requester name to be assigned to the Traffic change request ticket.
#     email:
#         required: true
#         description:
#             - The requester email to be assigned to the Traffic change request ticket.
#     source:
#         required: true
#         description:
#             - The hostname/nickname of the object that the network traffic will be sent from.
#             - For example: 192.168.1.5, PAYROLL_WEB_SERVER
#     dest:
#         required: true
#         description:
#             - The hostname/nickname of the network object that the network traffic will be sent to.
#             - For example: 192.168.1.5, PAYROLL_WEB_SERVER
#     service:
#         required: true
#         description:
#             - The service we want to check connectivity for (e.g. tcp/5000, ssh, https, udp/333).
#     # action:
#     #     default: allow
#     #     choices: [ allow, drop ]
#     #     description:
#     #         - Set the check for allowing network traffic or dropping network traffic.
#     transport:
#         default: ipv4
#         choices: [ ipv4, ipv6 ]
#         description:
#             - Set the network connectivity check transport layer type.
#
# requirements:
#     - requests==2.18.2
#     - suds-jurko==0.6
#     - suds_requests==0.3.1
# """
#
# EXAMPLES = """
# - hosts: localhost
#   tasks:
#     - name: Create FireFlow ticket if needed
#       # The best practice is to run only once, since only one ticket is needed
#       run_once: true
#       # Delegating the command to localhost, where we have access to Algosec Servers
#       delegate_to: localhost
#       aff_allow_traffic:
#         # Those parameters should be passed as args and loaded somewhere else, probably from the vault
#         algosec_host: 192.168.58.128
#         user: admin
#         password: VeryStrongPassword1#
#
#         # Specific connectivity check parameters
#         requestor: almogco
#         email: almog@company.com
#         source: 192.168.1.1
#         dest: 8.8.8.8
#         service: http
# """
#
# RETURN = """
# is_traffic_allowed:
#     description: True if the service traffic is allowed from source to dest
#     returned:
#         - always
#     type: bool
#     sample: True, False
# connectivity_status:
#     description: The string representing the connectivity status
#     returned:
#         - always
#     type: string
#     sample: Partially, Allowed, Blocked
# change_request_url:
#     description: URL to the generated Change Request Ticket on Algosec's servers
#     returned:
#         - on traffic change creation
#     type: string
#     sample: https://192.168.58.128/FireFlow/Ticket/Display.html?id=2410
# """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception


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
            changed = True

        module.exit_json(changed=changed, msg="Done!")

    except AlgosecAPIError:
        exc = get_exception()
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
