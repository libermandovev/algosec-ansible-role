AlgoSec Ansible Role
====================

DEPRECATED

|docs| |travis| |coverage|

.. |docs| image:: https://readthedocs.org/projects/algosec-ansible-role/badge/
   :target: http://algosec-ansible-role.readthedocs.io/en/latest/
   :alt: Documentation Status

.. |coverage| image:: https://img.shields.io/codecov/c/github/algosec/algosec-ansible-role.svg
    :target: https://codecov.io/gh/algosec/algosec-ansible-role

.. |travis| image:: https://travis-ci.com/algosec/algosec-ansible-role.svg?branch=master
    :target: https://travis-ci.com/algosec/algosec-ansible-role

Ansible role to DevOps-ify network security management, leveraging AlgoSec's business-driven security policy management solution

Documentation available online at: http://algosec-ansible-role.readthedocs.io/en/latest/

Requirements
------------

* This module is supported and fully tested under ``python2.7`` and ``python3.6``.

* All modules of this role require environment::

    pip install algosec --upgrade
    pip install ansible marshmallow urllib3

Installation
------------
The Ansible role can be installed directly from Ansible Galaxy by running::

    ansible-galaxy install algosec.algosec

If the ``ansible-galaxy`` command-line tool is not available (usually shipped with Ansible), or you prefer to download the role package directly,
navigate to the Ansible Galaxy `role page <https://galaxy.ansible.com/algosec/algosec/>`_ and hit "Download".

Alternately, you can directly navigate to our `GitHub repository <https://github.com/algosec/algosec-ansible-role>`_.

Usage
--------------

Once installed, you can start using the modules included in this role in your ansible playbooks.

To quickly get up and running a simple example you can follow these steps:

1. Download and unzip locally the examples folder by clicking `here <https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/algosec/algosec-ansible-role/tree/master/examples>`_.
2. Update authentication credentials in ``vars/algosec-secrets.yml``.
3. Update your AlgoSec server IP in ``inventory.ini``.
4. Update the arguments of the relevant modules in one of the playbooks (files with the ``yml`` extension).
5. Run ``ansible-playbook -i inventory.ini <playbook-filename>.yml``.
6. You've made it!


Documentation
-------------

.. image:: https://readthedocs.org/projects/algosec-ansible-role/badge/
   :target: https://algosec-ansible-role.readthedocs.io/en/latest/
   :alt: Documentation Status

Documentation available online at: https://algosec-ansible-role.readthedocs.io/en/latest/

How to build doc's locally?
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using Docker, running from one folder outside of the project::

    $ docker run -it -v $PWD/ansible-role-algosec/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make html

Using Spinx::

    $ cd docs
    $ make html

Then see the ``docs/_build`` folder created for the html files.

License
-------

MIT (see full license `here <http://algosec-ansible-role.readthedocs.io/en/latest/license.html>`_)

Author Information
------------------

AlgoSec Official Website
https://www.algosec.com/

Development
-----------

To kickoff local development, just use `pipenv`::

    pipenv install
    
And to use the newly installed virtual environment just run::

    pipenv shell

