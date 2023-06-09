# Osbuild Composer Ansible Collection

[![GitHub Super-Linter](https://github.com/redhat-cop/infra.osbuild/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)[![Codecov](https://img.shields.io/codecov/c/github/redhat-cop/infra.osbuild)](https://codecov.io/gh/redhat-cop/infra.osbuild)

[Ansible Collection](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
for management of [osbuild composer](https://www.osbuild.org/documentation/#composer)
to build [rpm-ostree](https://rpm-ostree.readthedocs.io/en/latest/) based
images for Fedora, Red Hat Enterprise Linux, and Centos Stream.
This collection has roles to build an osbuild server, an apache httpd server
to host images, and a role to build installer images and rpm-ostree updates.

## Installing

To install this collection and its dependencies, you will need to use the
[Ansible](https://github.com/ansible/ansible) `ansible-galaxy` command:

```shell
ansible-galaxy collection install git+https://github.com/redhat-cop/infra.osbuild
```

## How to use

You will need a RHEL, Centos Stream, or Fedora system that you can connect to
remotely via `ssh`, and a playbook to call the desired roles to result in the
desired functionality. Each role has it's own documentation specific to its
provided automation.

To use the example playbooks provided in this repository, please create an
inventory file that only has the osbuild build server(s) listed in them as these
example playbooks use the `all` Ansible [group](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups)
as the [host patten](https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html).

### Configure Osbuild Builder

```shell
ansible-playbook playbooks/osbuild_setup_server.yml
```

### Build an Image

```shell
ansible-playbook playbooks/osbuild_builder.yml
```

You can specify what kind of build you prefer with the variable buidler_compose_type.

Current supported and tested build types are:

- edge-commit
- edge-container
- edge-installer
- edge-simplified-installer
- edge-raw-image
- iot-commit (fedora only)
- iot-container (fedora only)
- iot-installer (fedora only)
- iot-raw-image (fedora only)

Example:

```shell
ansible-playbook playbooks/osbuild_builder.yml -e builder_compose_type=edge-installer
```

### Image Hosting

Images are hosted via apache http server that is setup using the setup_server playbook.
The images are located at this path on the osbuild server: `/var/www/html/<blueprint_name>/images`.
Inside the image directory will be version subdirectories for each iso built.

### Kickstart Hosting

Image kickstart files are also hosted that can be used as a boot option
via http on the osbuild server. The path is `http://<ip_addr>/<blueprint_name>/kickstart.ks`

### Auditing versions

You can run `rpm-ostree status` to see what specific version the system is using.

Here is a sample output:

```
Deployments:
* edge:rhel/8/x86_64/edge
    Version: 0.0.1 (2023-04-07T19:40:08Z)
    Commit: 7d3461f2fce7572fcdc9b3e8f75677bcdf96afed1ff5a3953f81852aad51f78d
```

## Supported Versions of Ansible

<!--start requires_ansible-->

## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.12**.

Plugins and modules within a collection may be tested with only specific
Ansible versions.  A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.

<!--end requires_ansible-->

## Tested with Ansible

- ansible-core 2.14 (devel)
- ansible-core 2.13 (stable)
- ansible-core 2.12 (stable)

## Code of Conduct

Please see the official [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).

## Licensing

[GNU General Public License v3.0 or later](https://github.com/redhat-cop/infra.osbuild/blob/main/LICENSE)
