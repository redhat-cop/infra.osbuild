#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -o pipefail -eux

declare -a args
IFS='/:' read -ra args <<< "$1"

ansible_version="${args[0]}"
script="${args[1]}"

function join {
    local IFS="$1";
    shift;
    echo "$*";
}

# Ensure we can write other collections to this dir
sudo chown "$(whoami)" "${PWD}/../../"

test="$(join / "${args[@]:1}")"

docker images ansible/ansible
docker images quay.io/ansible/*
docker ps

for container in $(docker ps --format '{{.Image}} {{.ID}}' | grep -v -e '^drydock/' -e '^quay.io/ansible/azure-pipelines-test-container:' | sed 's/^.* //'); do
    docker rm -f "${container}" || true  # ignore errors
done

docker ps

if [ -d /home/shippable/cache/ ]; then
    ls -la /home/shippable/cache/
fi

command -v python
python -V

function retry
{
    # shellcheck disable=SC2034
    for repetition in 1 2 3; do
        set +e
        "$@"
        result=$?
        set -e
        if [ ${result} == 0 ]; then
            return ${result}
        fi
        echo "@* -> ${result}"
    done
    echo "Command '@*' failed 3 times!"
    exit 255
}

command -v pip
pip --version
pip list --disable-pip-version-check
if [ "${ansible_version}" == "devel" ]; then
    retry pip install https://github.com/ansible/ansible/archive/devel.tar.gz --disable-pip-version-check
else
    retry pip install "https://github.com/ansible/ansible/archive/stable-${ansible_version}.tar.gz" --disable-pip-version-check
fi

export ANSIBLE_COLLECTIONS_PATHS="${PWD}/../../../"

if [ "${test}" == "sanity/extra" ]; then
    retry pip install junit-xml --disable-pip-version-check
fi

# START: HACK install dependencies
if [ "${script}" != "sanity" ] || [ "${test}" == "sanity/extra" ]; then
    # Nothing further should be added to this list.
    # This is to prevent modules or plugins in this collection having a runtime dependency on other collections.
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/community.internal_test_tools.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/internal_test_tools"
    # NOTE: we're installing with git to work around Galaxy being a huge PITA (https://github.com/ansible/galaxy/issues/2429)
    # retry ansible-galaxy -vvv collection install community.internal_test_tools
fi

if [ "${script}" != "sanity" ] && [ "${script}" != "units" ] && [ "${test}" != "sanity/extra" ]; then
    CRYPTO_BRANCH=main
    if [ "${script}" == "linux" ] && [[ "${test}" =~ "ubuntu1604/" ]]; then
        CRYPTO_BRANCH=stable-1
    fi
    # To prevent Python dependencies on other collections only install other collections for integration tests
    # NOTE: we're installing with git to work around Galaxy being a huge PITA (https://github.com/ansible/galaxy/issues/2429)

    # retry ansible-galaxy -vvv collection install ansible.posix
    retry git clone --depth=1 --single-branch https://github.com/ansible-collections/ansible.posix.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/ansible/posix"

    # retry ansible-galaxy -vvv collection install community.crypto
    retry git clone --depth=1 --branch "${CRYPTO_BRANCH}" --single-branch https://github.com/ansible-collections/community.crypto.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/crypto"

    # retry ansible-galaxy -vvv collection install community.general
    retry git clone --depth=1 --single-branch --single-branch https://github.com/ansible-collections/community.general.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/general"

    # retry ansible-galaxy -vvv collection install community.libvirt
    retry git clone --depth=1 --single-branch --single-branch https://github.com/ansible-collections/community.libvirt.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/community/libvirt"

    # retry ansible-galaxy -vvv collection install amazon.aws
    retry git clone --depth=1 --single-branch --single-branch https://github.com/ansible-collections/amazon.aws.git "${ANSIBLE_COLLECTIONS_PATHS}/ansible_collections/amazon/aws"
fi

# END: HACK

export PYTHONIOENCODING='utf-8'

if [ "${JOB_TRIGGERED_BY_NAME:-}" == "nightly-trigger" ]; then
    COVERAGE=yes
    COMPLETE=yes
fi

if [ -n "${COVERAGE:-}" ]; then
    # on-demand coverage reporting triggered by setting the COVERAGE environment variable to a non-empty value
    export COVERAGE="--coverage"
elif [[ "${COMMIT_MESSAGE}" =~ ci_coverage ]]; then
    # on-demand coverage reporting triggered by having 'ci_coverage' in the latest commit message
    export COVERAGE="--coverage"
else
    # on-demand coverage reporting disabled (default behavior, always-on coverage reporting remains enabled)
    export COVERAGE="--coverage-check"
fi

if [ -n "${COMPLETE:-}" ]; then
    # disable change detection triggered by setting the COMPLETE environment variable to a non-empty value
    export CHANGED=""
elif [[ "${COMMIT_MESSAGE}" =~ ci_complete ]]; then
    # disable change detection triggered by having 'ci_complete' in the latest commit message
    export CHANGED=""
else
    # enable change detection (default behavior)
    export CHANGED="--changed"
fi

if [ "${IS_PULL_REQUEST:-}" == "true" ]; then
    # run unstable tests which are targeted by focused changes on PRs
    export UNSTABLE="--allow-unstable-changed"
else
    # do not run unstable tests outside PRs
    export UNSTABLE=""
fi

# remove empty core/extras module directories from PRs created prior to the repo-merge
find plugins -type d -empty -print -delete

if [[ "${COVERAGE:-}" == "--coverage" ]]; then
    timeout=60
else
    timeout=50
fi

ansible-test env --dump --show --timeout "${timeout}" --color -v

"tests/utils/shippable/${script}.sh" "${test}" "${ansible_version}"
