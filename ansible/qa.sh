#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$script_dir/.."

yamllint . --strict --config-file ansible/.yamllint.yaml
cd "$script_dir"
ansible-playbook site.yaml --inventory development.ini.example --syntax-check
ansible-lint site.yaml ../tests/php85.yaml roles/pi/tests/settings_smoke.yaml roles/nvm/tests/smoke.yaml \
  --config-file .ansible-lint
