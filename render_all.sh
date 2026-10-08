#!/usr/bin/env bash
# Render via captured SVG, then rasterize and verify before replacing final images.
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python3 "$repo_dir/tools/render_diagrams.py"
python3 "$repo_dir/tools/check_course.py"
