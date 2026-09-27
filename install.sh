#!/usr/bin/env bash
# Install the meat-proxy skill by symlinking this repo into a skills directory.
#
#   ./install.sh            -> ~/.agents/skills/meat-proxy
#   ./install.sh --claude   -> also ~/.claude/skills/meat-proxy
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

link() {
  local target="$1"
  local parent
  parent="$(dirname "$target")"
  mkdir -p "$parent"

  if [ -L "$target" ]; then
    rm -f "$target"
  elif [ -e "$target" ]; then
    echo "refusing to overwrite existing non-symlink: $target" >&2
    echo "move it aside and re-run." >&2
    exit 1
  fi

  ln -sfn "$REPO_DIR" "$target"
  echo "linked $target -> $REPO_DIR"
}

link "$HOME/.agents/skills/meat-proxy"

if [ "${1:-}" = "--claude" ]; then
  link "$HOME/.claude/skills/meat-proxy"
fi

echo "done. restart your agent to pick up the skill."
