#!/usr/bin/env bash
# Install the bestpaper-writing skill for Claude, Codex, and/or Gemini.
# Usage: ./install.sh [claude|codex|gemini|all] [--project]
#   claude   -> ~/.claude/skills/bestpaper-writing        (--project: ./.claude/skills/)
#   codex    -> ~/.agents/skills/bestpaper-writing        (--project: ./.agents/skills/)
#   gemini   -> ~/.gemini/config/skills/bestpaper-writing (--project: ./.gemini/skills/)
set -euo pipefail
target="${1:-all}"; scope="${2:-}"
src="$(cd "$(dirname "$0")" && pwd)/skills/bestpaper-writing"
[ -f "$src/SKILL.md" ] || { echo "SKILL.md not found in $src" >&2; exit 1; }
install_to() {
  local dir="$1"
  local dst="$dir/bestpaper-writing"
  local user_mem="$dst/references/memory/user_memory.jsonl"
  local bak=""
  mkdir -p "$dir"
  if [ -f "$user_mem" ]; then
    bak="$(mktemp)"
    cp "$user_mem" "$bak"
  fi
  rm -rf "$dst"
  cp -R "$src" "$dst"
  rm -rf "$dst/scripts/__pycache__" "$dst/references/memory/paper_memory.db"
  if [ -n "$bak" ]; then
    mkdir -p "$dst/references/memory"
    mv "$bak" "$user_mem"
    echo "Preserved existing user_memory.jsonl in $dst"
  fi
  echo "Installed to $dst"
}
if [ "$scope" = "--project" ]; then claude_dir=".claude/skills"; codex_dir=".agents/skills"; gemini_dir=".gemini/skills"
else claude_dir="$HOME/.claude/skills"; codex_dir="$HOME/.agents/skills"; gemini_dir="$HOME/.gemini/config/skills"; fi
case "$target" in
  claude) install_to "$claude_dir" ;;
  codex)  install_to "$codex_dir" ;;
  gemini) install_to "$gemini_dir" ;;
  all)    install_to "$claude_dir"; install_to "$codex_dir"; install_to "$gemini_dir" ;;
  *) echo "Usage: $0 [claude|codex|gemini|all] [--project]" >&2; exit 1 ;;
esac
echo "Restart your agent if the skill does not show up."
