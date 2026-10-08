#!/usr/bin/env bash
# Compatibility entry point: render all course diagrams.
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$repo_dir/render_all.sh"
