# Osbuild Composer Ansible Collection

[![GitHub Super-Linter](https://github.com/redhat-cop/infra.osbuild/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

[Ansible Collection](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for management of [osbuild composer](https://www.osbuild.org/documentation/#composer) 
to build ostree based images for Fedora, Red Hat Enterprise Linux and Centos Stream. This collection has roles to build an osbuild server, an apache server to host images and roles to build images and updates.

## Installing

To install this collection and its dependencies, you will need to use the [Ansible](https://github.com/ansible/ansible) `ansible-galaxy` command:

```shell
ansible-galaxy collection install git+https://github.com/redhat-cop/infra.osbuild
```

## How to use

You will need a RHEL, Centos Stream or Fedora server that you can connect to remotely via an inventory, or run this collection locally by changing the playbooks to hosts: localhost instead of all.

### Configure Osbuild Composer Server

```shell
ansible-playbook playbooks/osbuild_setup_server.yml
```

### Configure Osbuild Builder (this will also host the images)

```shell
ansible-playbook playbooks/osbuild_builder.yml
```
You can specify what kind of build you prefer with the variable buidler_compose_type. The options for this are:

- ami
- edge-commit
- edge-container
- edge-installer
- edge-raw-image
- edge-simplified-installer
- image-installer
- oci
- openstack
- qcow2
- tar
- vhd
- vmdk
- iot-commit (fedora only)
- iot-container (fedora only)
- iot-installer (fedora only)
- iot-raw-image (fedora only)
- container

Example:

```shell
ansible-playbook playbooks/osbuild_builder.yml -e builder_compose_type=qcow2
```

### Configure testbuild

Provide type of image you would like to compose in format of compose_type=typename

For RHEL/Centos valid types are: valid types are: ami, container, edge-commit, edge-container, edge-installer, edge-raw-image, oci, openstack, qcow2, vhd, vmdk

For Fedora valid types are: ami, container, iot-commit, iot-container, iot-installer, iot-raw-image, oci, openstack, qcow2, vhd, vmdk

Example:
```shell
ansible-playbook playbooks/testbuild.yml -e builder_compose_type=edge-installer
```
