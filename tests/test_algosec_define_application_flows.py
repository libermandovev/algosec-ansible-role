import pytest

from library import algosec_define_application_flows
from tests.conftest import (
    AnsibleExitJson,
    ALGOSEC_SERVER,
    ALGOSEC_USER,
    ALGOSEC_PASSWORD,
    ALGOSEC_CERTIFY_SSL,
    my_vcr,
    AnsibleFailJson,
)

# Used to clean all flows from the ABF application for the rest of the tests to be deterministic
DELETE_ALL_FLOWS_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    app_name="TEST2",
    check_connectivity=True,
    app_flows={}
)

PROPER_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    app_name="TEST2",
    check_connectivity=True,
    app_flows={
        "flow-that-will-change": {
            "sources": ["192.168.12.12", "HR Payroll server", "192.168.0.0/16"],
            "destinations": ["16.47.71.62", "234.234.234.234"],
            "services": ["HTTPS", "http", "tcp/80", "tcp/51"]
        },
        "flow-that-will-be-deleted": {
            "sources": ["192.168.2.1"],
            "destinations": ["192.168.2.2"],
            "services": ["tcp/200"]
        },
        "another-flow-that-will-be-deleted": {
            "sources": ["192.168.12.1"],
            "destinations": ["192.168.12.3"],
            "services": ["tcp/201"]
        },
        "flow-that-will-not-change": {
            "sources": ["10.0.0.1"],
            "destinations": ["10.0.0.2"],
            "services": ["udp/501"]
        }
    }
)

PROPER_ARGS2 = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    app_name="TEST2",
    app_flows={
        "flow-that-will-change": {
            "sources": ["HR Payroll server", "192.168.0.0/16"],
            "destinations": ["16.47.71.62"],
            "services": ["HTTPS"]
        },
        "flow-that-will-not-change": {
            "sources": ["10.0.0.1"],
            "destinations": ["10.0.0.2"],
            "services": ["udp/501"]
        },
        "second-run-new-flow": {
            "sources": ["1.2.3.4"],
            "destinations": ["3.4.5.6"],
            "services": ["SSH"]
        }
    }
)

PROPER_ARGS2__WITH_CONNECTIVITY_CHECK = PROPER_ARGS2.copy()
PROPER_ARGS2__WITH_CONNECTIVITY_CHECK['check_connectivity'] = True


# TODO: Add tests for checkmode
# TODO: Add tests for proper/improper module arguments
# TODO: Add tests for missing algosec package
class TestDefineApplicationFlows(object):
    ansible_module = algosec_define_application_flows

    # TODO: Add tests to verify that an application would be created if this is the first request to it
    @pytest.mark.parametrize('ansible_module_args', [DELETE_ALL_FLOWS_ARGS], indirect=True)
    @my_vcr.use_cassette('define_application_flows__clearing_all_flows.yaml')
    def test_delete_all_flows_from_application(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['msg'] == 'App flows updated successfully and application draft was applied!'
        assert return_value['changed']

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS], indirect=True)
    @my_vcr.use_cassette('define_application_flows__creating_new_flows.yaml')
    def test_create_new_flows_in_application(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['changed']
        assert return_value['created_flows'] == 4
        assert return_value['deleted_flows'] == 0
        assert return_value['modified_flows'] == 0
        assert return_value['unchanged_flows'] == 0
        assert return_value['msg'] == 'App flows updated successfully and application draft was applied!'

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS2], indirect=True)
    @my_vcr.use_cassette('define_application_flows__changing_flows.yaml')
    def test_change_application_flows__connectivity_check_pass(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['changed']
        assert return_value['created_flows'] == 1
        assert return_value['deleted_flows'] == 2
        assert return_value['modified_flows'] == 1
        assert return_value['unchanged_flows'] == 1
        assert return_value['msg'] == 'App flows updated successfully and application draft was applied!'

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS2__WITH_CONNECTIVITY_CHECK], indirect=True)
    @my_vcr.use_cassette('define_application_flows__changing_flows__connectivity_check_fail.yaml')
    def test_change_application_flows__but_connectivity_check_fail(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleFailJson) as result:
            ansible_module.main()
        exception_return_value = result.value.args[0]
        assert exception_return_value['changed']
        assert exception_return_value['created_flows'] == 1
        assert exception_return_value['deleted_flows'] == 2
        assert exception_return_value['modified_flows'] == 1
        assert exception_return_value['unchanged_flows'] == 1
        assert exception_return_value['msg'] == 'Flows defined successfully but connectivity check failed.'

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS2], indirect=True)
    @my_vcr.use_cassette('define_application_flows__not_changing_flows.yaml')
    def test_no_change_when_same_definition_applied_twice(self, ansible_module_args, ansible_module):
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert not return_value['changed']
        assert return_value['created_flows'] == 0
        assert return_value['deleted_flows'] == 0
        assert return_value['modified_flows'] == 0
        assert return_value['unchanged_flows'] == 3
        assert return_value['msg'] == 'Application flows are up-to-date on on AlgoSec BusinessFlow.'

    # TODO: Verify the flows status on the server just by using the client
    # TODO: at the end of the round to see that we have to proper state on ABF
