#!/usr/bin/env bash

set -euox pipefail

start=`date +%s`
script_dir=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd ${script_dir}

time yamllint . --strict --config-file .yamllint.yaml
time ansible-playbook site.yaml --inventory development.ini.example --syntax-check
time ANSIBLE_DEPRECATION_WARNINGS=False ansible-lint site.yaml --config-file .ansible-lint
#time molecule test

cd -
end=`date +%s`
finished_in_seconds=$((end-start))
