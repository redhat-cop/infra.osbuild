#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH="../;/roles:/usr/share/ansible/roles:/etc/ansible/roles" ansible-playbook "${ANSIBLE_PLAYBOOK_DIR}/tasks/main.yml" -i "../../inventory" "$@"
