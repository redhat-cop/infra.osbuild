#!/usr/bin/env bash

set -o pipefail -eux

echo "${PATH/\~/${HOME}}"
echo "${HOME}"
command -v ansible

pip install --upgrade pip
pip install --upgrade ansible-lint

PATH="${PATH/\~/${HOME}}" ansible-lint --profile=production
