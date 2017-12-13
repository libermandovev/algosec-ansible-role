Algosec Ansible Role
====================

Algosec Ansible role provide a set of Ansible modules to help you manage and orchestrate your work with the different Algosec services.

Requirements
------------

All modules of this role are dependent upon the `algosec` python package which is distributed separately::

    pip install algosec

Role Variables
--------------

See documentation for using the specific modules.

Example Playbook
----------------

See documentation for using the specific modules.

License
-------

BSD

Author Information
------------------

Algosec Official Website
https://www.algosec.com/


Installation
------------
::

    ansible-galaxy install Algosec.algosec


Development
-----------

First create a virtual environment for the project::

    mkvirtualenv algosecansibleenv
    
Install the requirements for the project::

    pip install -r requirements.txt

Debug
-----
::

    pip install ipdb
    python -m ipdb ./library/abf_flow.py ./debug/abf_flow_args.json
    
and the `abf_flow_args.json` file should look something like::

    {
      "ANSIBLE_MODULE_ARGS": {
        "ip_address": "192.168.58.128",
        "user": "admin",
        "password": "SomePassword",
        "app_name": "Payroll",
        "name": "new-test-flow",
        "sources": "192.168.12.12",
        "destinations": "10.40.22.10"
      }
    }

It should match the playbook module used of course.


Documentation
-------------

**How to build doc's locally?**
    
Using Docker::

    $ docker run -it -v $PWD:/ansible-role-algosec/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make html

Using Spinx::

    $ cd docs
    $ make html
