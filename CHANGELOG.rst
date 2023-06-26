===========================
Infra.Osbuild Release Notes
===========================

.. contents:: Topics


v2.1.0
======

Release Summary
---------------

Adds new populate_aap, system_info, and update_systems roles,
AWS as a hosted osbuild server, survey questions, substantial enhancements to the
builder role and weldr interface, and a large number of bugfixes, test, security,
documentation, and environment stabilization enhancements.

Major Changes
-------------

- Add AWS as an hosted osbuild server
- Add populate_aap role
- builder - added new versions image directory structure. From /blueprint_name/images to /blueprint_name/images/version
- system_info - created new role to gather information from a running rpm-ostree based system
- update_systems - created new role to update system to the latest commit / image

Minor Changes
-------------

- Add Clear package cache and restart service steps to the builder role
- Add first set of survey questions for builder role
- Add more survey questions
- Added argument specification file to validate arguments supplied to builder role
- Added system info and update system to populate_aap role
- Allow builds with existing ostree commit (skipping building a commit)
- When HTTP errors occur, display message body so user has more context
- builder - added ability to remove all images when builder_image_storage_cleared is true
- builder - added builder_wait_compose_timeout to control how long the timeout is set to.
- builder - added check to see if image storage is full based on threshold percentage using the builder_image_store_threshold variable.
- builder - added enforce_auth to fail when no ssh key or password is defined. Can be set to false to bypass auth for image.
- builder - allowed for passing aap vars to the role will generate the corresponding template instead of doing this manually.
- builder - builder_pub_key is for raw ssh keys
- builder - created builder_pub_key_path for ssh key lookups
- builder - use blueprint for builder_password not kickstart
- weldr - added get_job_id using image compose_id to allow us to identify images inside osbuild artifacts

Bugfixes
--------

- Fix "UnknownUUID is not a valid UUID" issue
- Fix improper file extension issue which causes playbook runs to fail
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/123
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/127
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/209
- Fix issue with image building by getting the body
- Fix issue with weldr post compose status_code
- Fixes ansible-lint errors which prevented Azure Pipelines from passing (AAP-12274)
- Fixes issue https://github.com/redhat-cop/infra.osbuild/issues/119
- Fixes multiple file searching in /etc/yum.repos.d/
- builder - fixed bug where passing the env arg builder_compose_type to the playbook overrided an internal variable causing the build to fail.
- compose_wait - fixes timeout to fail if timeout is reached.

Documentation Changes
---------------------

- Added 1.0.0 release notes
- Added docs for image hosting
- Added docs for kickstart hosting

v2.0.0
======

Release Summary
---------------

This release adds support for more compose types, ostree-based OS, Ansible Execution Environment (AEE),
cross-distribution composes, RHSM repositories, and kickstart support (including Ansible Authomation
Platform (AAP) auto-registration and custom template).
Documentation expanded for more compose_types and use cases
As always, we corrected a number of bugs.

Major Changes
-------------

- Add edge-installer to builder role
- Add role for building edge-installer ISOs using the modules within the collection
- Enable rpm-ostree ISO installer builds
- Fix compose types ami, edge-container, image-installer, oci, openstack, qcow2, vhd, vmdk, iot-commit, iot-container and container
- Modifies the setup_server role for use with an ostree-based operating system

Minor Changes
-------------

- Add Ansible Execution Environment (AEE)
- Add example playbook
- Add options and post section variables to kickstart template
- Add support for RHSM repositories
- Added kickstart file to auto register with Ansible Automation Platform (AAP)
- Allow edge-installer kickstart file to optionally use a custom Jinja2 template
- Allow user to skip repository update
- Change test cases to validate function
- Conditionally create AAP playbook if builder_aap_url is defined
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/85
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/98
- Handle cross-distro composes
- Remove Ansible Automation Platform (AAP) defaults
- Update builder README.md to provide example of AAP playbook added to kickstart file
- builder - added ability to validate kickstart after creation of file

Bugfixes
--------

- Conditionally add sshkey and/or user password to kickstart file if defined
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/108
- Fix issue https://github.com/redhat-cop/infra.osbuild/issues/74
- Fix issue where kickstart would not properly resolve hostnames
- Fixes issue https://github.com/redhat-cop/infra.osbuild/issues/97
- Resolve issue https://github.com/redhat-cop/infra.osbuild/issues/73
- Update testbuild playbook to new build flow and fix issue 38
- Warn if sshkey file is undefined
- builder - Fixed remove all images from storage task when UUID is an ID.
- builder - Fixes kickstart when passing none as an option to skip all omitted values

Documentation Changes
---------------------

- Added builder role documentation
- updated documentation to explain how to call different build types

v1.0.0
======

Release Summary
---------------

Initial release of infra.osbuild

Major Changes
-------------

- Add custom repositories as sources for blueprints
- Added get_all_finished_images module
- Added image_server role
- Added osbuild_server role
- Implement more weldrapiv1 methods

Minor Changes
-------------

- Add blueprint details (semantic versioning, name)
- Add rhsm (Red Hat Subscription Manager) option
- Add weldr socket timeout
- Change name from osbuild.composer to infra.osbuild (Validated Content)
