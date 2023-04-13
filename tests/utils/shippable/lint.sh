#!/usr/bin/env bash

set -o pipefail -eux

echo "${PATH}"
echo "${HOME}"
command -v ansible

pip install 'ansible-lint==6.14.4' --disable-pip-version-check

PATH="${PATH}:${HOME}/.local/bin" ansible-lint --profile=production
