import json
import os

import pytest
import vcr
from algosec.api_clients.business_flow import BusinessFlowAPIClient
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from mock import patch


ALGOSEC_PASSWORD = "algosec"
ALGOSEC_USER = "admin"
ALGOSEC_SERVER = "local.algosec.com"
ALGOSEC_CERTIFY_SSL = False


tests_dir = os.path.dirname(os.path.realpath(__file__))

my_vcr = vcr.VCR(
    # serializer='json',
    cassette_library_dir=os.path.join(tests_dir, 'fixtures/cassettes'),
    # record_mode='once',
    # match_on=['uri', 'method'],
)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith('my_command'):
        return '/usr/bin/my_command'
    else:
        if required:
            fail_json(msg='%r not found !' % arg)


@pytest.fixture(scope='function')
def ansible_module_args(request):
    """prepare arguments so that they will be picked up during module creation"""
    stringified_args = json.dumps({'ANSIBLE_MODULE_ARGS': request.param})
    with patch.object(basic, '_ANSIBLE_ARGS', to_bytes(stringified_args)):
        yield request.param


@pytest.fixture(scope='function')
def ansible_module(request):
    with patch.multiple(
        basic.AnsibleModule,
        exit_json=exit_json,
        fail_json=fail_json,
        get_bin_path=get_bin_path,
    ):
        with patch.object(basic.AnsibleModule, 'run_command'):
            yield request.param


def pytest_generate_tests(metafunc):
    if 'ansible_module' in metafunc.fixturenames:
        metafunc.parametrize('ansible_module', [metafunc.cls.ansible_module], indirect=True)


@pytest.fixture(scope='session')
def abf_client():  # type: () -> BusinessFlowAPIClient
    return BusinessFlowAPIClient(ALGOSEC_SERVER, ALGOSEC_USER, ALGOSEC_PASSWORD, ALGOSEC_CERTIFY_SSL)
