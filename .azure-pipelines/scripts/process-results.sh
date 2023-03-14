#!/usr/bin/env bash
# Check the test results and set variables for use in later steps.

set -o pipefail -eu

if [[ "$PWD" =~ /ansible_collections/ ]]; then
    output_path="tests/output"
else
    output_path="test/results"
fi

echo "##vso[task.setVariable variable=outputPath]${output_path}"

#touch "${output_path}"'/bot/file.tar'
mkdir -p "${output_path}"'/bot/'
#sudo mv "/root/ansible_collections/infra/osbuild/tests/images"'/*.tar' "${output_path}"'/bot/'

echo "Locations..."
pwd
echo "Searching..."
find ./ -name "*.tar"

if compgen -G "${output_path}"'/bot/*.tar' > /dev/null; then
    echo "There is images"
    ls "${output_path}"'/bot/'
else
    echo "There is no images"
fi

if compgen -G "${output_path}"'/junit/*.xml' > /dev/null; then
    echo "##vso[task.setVariable variable=haveTestResults]true"
fi

if compgen -G "${output_path}"'/bot/*' > /dev/null; then
    echo "There are bot results"
    echo "##vso[task.setVariable variable=haveBotResults]true"
fi

if compgen -G "${output_path}"'/coverage/*' > /dev/null; then
    echo "##vso[task.setVariable variable=haveCoverageData]true"
fi
