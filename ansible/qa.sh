#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$script_dir"

yamllint . --strict --config-file .yamllint.yaml
ansible-playbook site.yaml --inventory development.ini.example --syntax-check
ANSIBLE_DEPRECATION_WARNINGS=False ansible-lint site.yaml --config-file .ansible-lint
