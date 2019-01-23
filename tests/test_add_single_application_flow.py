import pytest
from algosec.errors import EmptyFlowSearch

from library import algosec_add_single_application_flow
from tests.conftest import AnsibleExitJson, ALGOSEC_SERVER, ALGOSEC_USER, ALGOSEC_PASSWORD, ALGOSEC_CERTIFY_SSL, my_vcr

PROPER_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    app_name="Payroll",
    name="new-test-flow-2",
    sources=["192.168.12.12", "HR Payroll server", "192.168.0.0/16"],
    destinations=["16.47.71.62", "234.234.234.234"],
    services=["HTTPS", "http", "tcp/80", "tcp/51"]
)


MODIFIED_FLOW_ARGS = dict(
    ip_address=ALGOSEC_SERVER,
    user=ALGOSEC_USER,
    password=ALGOSEC_PASSWORD,
    certify_ssl=ALGOSEC_CERTIFY_SSL,
    app_name="Payroll",
    name="new-test-flow-2",
    sources=["192.168.12.12", "HR Payroll server", "192.168.0.0/16"],
    destinations=["16.47.71.62", "234.234.234.234"],
    services=["HTTPS"]
)


class TestDefineApplicationFlows(object):
    ansible_module = algosec_add_single_application_flow

    @staticmethod
    def does_flow_exists(abf_client, app_name, flow_name):
        """Used to delete a flow on ABF to prepare for the tests"""
        app_revision_id = abf_client.get_application_revision_id_by_name(app_name)
        try:
            abf_client.get_flow_by_name(app_revision_id, flow_name)
            return True
        except EmptyFlowSearch:
            return False

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS], indirect=True)
    @my_vcr.use_cassette('add_single_application_flow_1.yaml')
    def test_create_new_application_flow(self, abf_client, ansible_module_args, ansible_module):
        app_name = ansible_module_args['app_name']
        flow_name = ansible_module_args['name']
        if self.does_flow_exists(abf_client, app_name, flow_name):
            raise UserWarning(
                "Please manually delete {} flow from {} ABF app, "
                "apply any drafts and resolve change requests for this unittest to properly run.".format(
                    flow_name,
                    app_name,
                )
            )
        # TODO: Test also creation of new network objects, by deleting some of the ones that are used
        # TODO: Very similar to how the flow deletion is taking place.
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['changed'], "'changed' should be True as a new flow was created on ABF."
        assert return_value['msg'] == 'Flow created/updated successfully!'
        # TODO: Add to the ansible output whether the flow was created or updated

    @pytest.mark.parametrize('ansible_module_args', [PROPER_ARGS], indirect=True)
    @my_vcr.use_cassette('add_single_application_flow_2.yaml')
    def test_not_creating_an_already_existing_flow(self, abf_client, ansible_module_args, ansible_module):
        app_name = ansible_module_args['app_name']
        flow_name = ansible_module_args['name']
        if not self.does_flow_exists(abf_client, app_name, flow_name):
            raise UserWarning(
                "Please run the `test_create_new_application_flow` unittest before running this unittest "
                "to make sure the flow already exists on ABF."
            )
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert not return_value['changed']
        assert return_value['msg'] == 'Flow already exists on AlgoSec BusinessFlow.'

    @pytest.mark.parametrize('ansible_module_args', [MODIFIED_FLOW_ARGS], indirect=True)
    @my_vcr.use_cassette('add_single_application_flow__changing_existing_flow.yaml')
    def test_changing_existing_flow(self, abf_client, ansible_module_args, ansible_module):
        app_name = ansible_module_args['app_name']
        flow_name = ansible_module_args['name']
        if not self.does_flow_exists(abf_client, app_name, flow_name):
            raise UserWarning(
                "Please run the `test_create_new_application_flow` unittest before running this unittest "
                "to make sure the flow already exists on ABF."
            )
        with pytest.raises(AnsibleExitJson) as result:
            ansible_module.main()
        return_value = result.value.args[0]
        assert return_value['changed']
        assert return_value['msg'] == 'Flow created/updated successfully!'
        # TODO: Add to the ansible output whether the flow was created or updated
