Algosec Ansible Role
====================

Algosec Ansible role provide a set of Ansible modules to help you manage and orchestrate your work with the different Algosec services.

Documentation available at: http://algosec-ansible-role.readthedocs.io/en/latest/

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

Documentation
-------------
Documentation available at: http://algosec-ansible-role.readthedocs.io/en/latest/

**How to build doc's locally?**
    
Using Docker::

    $ docker run -it -v $PWD:/ansible-role-algosec/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make html

Using Spinx::

    $ cd docs
    $ make html

