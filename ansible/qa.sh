#!/usr/bin/env bash

set -euox pipefail

start=`date +%s`

time yamllint . --strict --config-file .yamllint.yaml
time ansible-playbook site.yaml --inventory development.ini.example --syntax-check
time ansible-lint site.yaml --strict --config-file .ansible-lint
#time molecule test

end=`date +%s`
finished_in_seconds=$((end-start))
