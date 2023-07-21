#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH="/usr/share/ansible/roles" ansible-playbook tests/integration/targets/compose-type/edge_commit/tasks/main.yml -i ../../inventory "$@"
