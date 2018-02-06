Algosec Ansible Role
====================

Algosec Ansible role provides a set of Ansible modules to help you manage and orchestrate your work with the different Algosec services.

Documentation available online at: http://algosec-ansible-role.readthedocs.io/en/latest/

Installation
------------
::

    ansible-galaxy install algosec.algosec

Requirements
------------

All modules of this role are dependent upon the `algosec` python package which is distributed separately::

    pip install algosec
    pip install ansible

Documentation
-------------
How to build doc's locally?
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using Docker, running from one folder outside of the project::

    $ docker run -it -v $PWD/ansible-role-algosec/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make html

Using Spinx::

    $ cd docs
    $ make html

License
-------

BSD

Author Information
------------------

Algosec Official Website
https://www.algosec.com/

Development
-----------

First create a virtual environment for the project::

    mkvirtualenv algosecansibleenv
    
Install the requirements for the project::

    pip install -r requirements.txt

Debug
-----
First install ``ipdb`` for easier debugging process::

    pip install ipdb

abf_update_flow
^^^^^^^^^^^^^^^
Update the ``./debug/abf_update_flow_args.json`` file with your credentials and command arguments, then run::

    python -m ipdb ./library/abf_update_flow.py ./debug/abf_update_flow_args.json

aff_allow_traffic
^^^^^^^^^^^^^^^^^^
Update the ``./debug/aff_allow_traffic_args.json`` file with your credentials and command arguments, then run::

    python -m ipdb ./library/aff_allow_traffic.py ./debug/aff_allow_traffic_args.json
