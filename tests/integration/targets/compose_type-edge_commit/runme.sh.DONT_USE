#!/usr/bin/env bash

set -eux

# shellcheck disable=1091
source virtualenv.sh

ANSIBLE_ROLES_PATH=../:/usr/share/ansible/roles/ ansible-playbook "${ANSIBLE_PLAYBOOK_DIR}/runme.yml" -i "../../inventory" "$@"
