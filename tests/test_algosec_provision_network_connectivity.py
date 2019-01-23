import re

import pytest

from library import algosec_provision_network_connectivity
from tests.conftest import AnsibleExitJson, ALGOSEC_SERVER, ALGOSEC_PASSWORD, ALGOSEC_USER, ALGOSEC_CERTIFY_SSL, my_vcr

PROPER_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    requestor='algosec user',
    email='algosec@algosec.com',
    traffic_lines=[
        {
            "action": True,
            "sources": ["192.168.12.12", "123.123.132.123"],
            "destinations": ["16.47.71.62", "234.234.234.234"],
            "services": ["HTTPS", "http", "tcp/80", "tcp/51"]
        },
        {
            "action": False,
            "sources": ["10.0.0.1"],
            "destinations": ["10.0.1.0"],
            "services": ["HTTPS"]

        }
    ],
    # template='',
)


NO_CHANGE_REQUEST_NEEDED_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    requestor='algosec user',
    email='algosec@algosec.com',
    traffic_lines=[
        {
            "action": False,
            "sources": ["192.168.12.12", "123.123.132.123"],
            "destinations": ["16.47.71.62", "234.234.234.234"],
            "services": ["HTTPS", "http", "tcp/80", "tcp/51"]
        },
    ],
)


class TestProvisionNetworkConnectivity(object):
    ansible_module = algosec_provision_network_connectivity

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS], indirect=True)
    @my_vcr.use_cassette('provision_network_connectivity_1.yaml')
    def test_module_return_value(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['changed'] is True, \
            "'changed' should always be marked as True for this module as a Change Request is always created."
        assert re.match(
            r'https://192\.168\.58\.129/FireFlow/Ticket/Display\.html\?id=\d+',
            return_value['change_request_url']
        ) is not None, 'Invalid change request url provided in module result.'

    @pytest.mark.parametrize('ansible_module_args', [NO_CHANGE_REQUEST_NEEDED_ARGS], indirect=True)
    @my_vcr.use_cassette('provision_network_connectivity__no_change_request_needed.yaml')
    def test_no_change_request_is_needed(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert not return_value['changed']
