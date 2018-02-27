import traceback

import urllib3
from ansible.module_utils.basic import AnsibleModule

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from algosec.api_client import FirewallAnalyzerAPIClient, FireFlowAPIClient
    from algosec.errors import AlgoSecAPIError
    from algosec.models import DeviceAllowanceState, ChangeRequestAction

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            ip_address=dict(required=True),
            user=dict(required=True, aliases=["username"]),
            password=dict(aliases=["pass", "pwd"], required=True, no_log=True),
            certify_ssl=dict(type="bool", default=True),
            requestor=dict(required=True),
            email=dict(required=True),
            sources=dict(type="list", required=True),
            destinations=dict(type="list", required=True),
            services=dict(type="list", required=True),
        )
    )

    if not HAS_LIB:
        module.fail_json(msg="algoec package is required for this module")

    try:
        afa_client = FirewallAnalyzerAPIClient(
            module.params["ip_address"],
            module.params["user"],
            module.params["password"],
            module.params["certify_ssl"],
        )
        connectivity_status = afa_client.run_traffic_simulation_query(
            source=module.params["sources"],
            dest=module.params["destinations"],
            service=module.params["services"],
        )
    except AlgoSecAPIError:
        module.fail_json(msg="Error executing traffic simulation query:\n{}".format(traceback.format_exc()))
        return

    response = {}
    if connectivity_status == DeviceAllowanceState.ALLOWED:
        module.log("Connectivity check passed. No FireFlow change request is required")
        response["changed"] = False
    else:

        module.log(
            "Connectivity status is {}. Opening change request on AlgoSec FireFlow at {}".format(
                connectivity_status,
                module.params["ip_address"]
            )
        )
        if not module.check_mode:
            try:
                aff_client = FireFlowAPIClient(
                    module.params["ip_address"],
                    module.params["user"],
                    module.params["password"],
                    module.params["certify_ssl"],
                )
                requestor = module.params["requestor"]
                change_request_url = aff_client.create_change_request(
                    # TODO: drop action is not yet supported
                    action=ChangeRequestAction.ALLOW,
                    subject="Allow {} traffic from {} to {} (issued via Ansible)".format(
                        module.params["services"],
                        module.params["sources"],
                        module.params["destinations"]
                    ),
                    requestor_name=requestor,
                    email=module.params["email"],
                    sources=module.params["sources"],
                    destinations=module.params["destinations"],
                    services=module.params["services"],
                    description="Traffic change request created by {} directly from Ansible.".format(requestor)
                )
            except AlgoSecAPIError:
                module.fail_json(msg="Error creating change request:\n{}".format(traceback.format_exc()))
                return
            response["change_request_url"] = change_request_url
        response["changed"] = True

    module.exit_json(**response)


if __name__ == "__main__":
    main()
