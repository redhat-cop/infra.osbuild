#!/usr/bin/env bash

set -o pipefail -eux

echo "${PATH/\~/${HOME}}"
echo "${HOME}"
command -v ansible

pip install ansible-lint --disable-pip-version-check

PATH="${PATH/\~/${HOME}}" ansible-lint --profile=production
