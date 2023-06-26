===========================
Infra.Osbuild Release Notes
===========================

.. contents:: Topics


v2.0.0
======

Release Summary
---------------

Adds support for more compose types, ostree-based OS, Ansible Execution Environment (AEE),
cross-distribution composes, RHSM repositories, and kickstart support (including Ansible Authomation
Platform (AAP) auto-registration and custom template).
Documentation expanded for more compose_types and use cases
Additionally, corrected a number of bugs.

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
