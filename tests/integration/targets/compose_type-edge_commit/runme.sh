#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH="/usr/share/ansible/roles" ansible-playbook "${ANSIBLE_PLAYBOOK_DIR}/targets/compose_type-edge_commit/tasks/main.yml" -i "../../inventory" "$@"
