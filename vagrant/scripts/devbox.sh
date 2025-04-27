#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: $CONFIG_FILE not found."
  exit 1
fi

provider=$(grep -o '"provider"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_FILE" | sed -E 's/.*"([^"]*)"/\1/')

if [ -z "${provider:-}" ]; then
  provider="virtualbox"
fi

if [ "$provider" != "virtualbox" ] && [ "$provider" != "libvirt" ]; then
  echo "Error: Unsupported provider '$provider' in config.json."
  exit 1
fi

VAGRANT_DEFAULT_PROVIDER="$provider" vagrant "$@"
