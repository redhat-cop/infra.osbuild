Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Custom Repositories
-------------------

To add a custom repository you need to specify the following variables per repo. custom_repo_name, custom_repo_base_url, custom_repo_type, custom_repo_check_ssl, custom_repo_check_gpg, custom_repo_state.

Example vars file:

```bash
custom_repo_name: Everything
custom_repo_base_url: https://dl.fedoraproject.org/pub/epel/9/Everything/x86_64/
custom_repo_type: yum-baseurl
custom_repo_check_ssl: false
custom_repo_check_gpg: false
custom_repo_state: present
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPLv3+

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
