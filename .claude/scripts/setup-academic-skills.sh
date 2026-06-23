#!/usr/bin/env bash
# Install community academic-writing skills into ~/.claude/skills/.
#
# Skills installed:
#   - academic-research-skills (Imbad0202)  CC-BY-NC 4.0
#       deep-research, academic-paper, academic-paper-reviewer, academic-pipeline
#   - academic-paper-skills (lishix520)
#       academic-paper-strategist, academic-paper-composer
#   - econ-writing-skill (hanlulong)
#       econ-write
#
# Usage:  bash .claude/scripts/setup-academic-skills.sh
#         bash .claude/scripts/setup-academic-skills.sh --update
#
# After running, restart Claude Code (or /reload-plugins) so the skills appear.

set -euo pipefail

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
SRC_DIR="$SKILLS_DIR"
UPDATE=0

for arg in "$@"; do
  case "$arg" in
    --update|-u) UPDATE=1 ;;
    --help|-h)
      sed -n '2,18p' "$0"
      exit 0 ;;
  esac
done

mkdir -p "$SKILLS_DIR"

clone_or_pull() {
  local url="$1" dir="$2"
  if [ -d "$SRC_DIR/$dir/.git" ]; then
    if [ "$UPDATE" -eq 1 ]; then
      echo ">> updating $dir"
      git -C "$SRC_DIR/$dir" pull --ff-only
    else
      echo ">> $dir already present (use --update to refresh)"
    fi
  else
    echo ">> cloning $dir"
    git clone --depth 1 "$url" "$SRC_DIR/$dir"
  fi
}

link() {
  local target="$1" name="$2"
  ln -sfn "$target" "$SKILLS_DIR/$name"
  echo "   linked: $name -> $target"
}

clone_or_pull https://github.com/Imbad0202/academic-research-skills.git academic-research-skills-src
clone_or_pull https://github.com/lishix520/academic-paper-skills.git    academic-paper-skills-src
clone_or_pull https://github.com/hanlulong/econ-writing-skill.git       econ-writing-skill-src

link academic-research-skills-src/deep-research            deep-research
link academic-research-skills-src/academic-paper           academic-paper
link academic-research-skills-src/academic-paper-reviewer  academic-paper-reviewer
link academic-research-skills-src/academic-pipeline        academic-pipeline
link academic-paper-skills-src/strategist                  academic-paper-strategist
link academic-paper-skills-src/composer                    academic-paper-composer
link econ-writing-skill-src/.claude/skills/econ-write      econ-write

# zh-en-academic: copy from repo if available, otherwise skip
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../.." && pwd)"
if [ -d "$REPO_ROOT/.claude/skills/zh-en-academic" ]; then
  rm -rf "$SKILLS_DIR/zh-en-academic"
  cp -r "$REPO_ROOT/.claude/skills/zh-en-academic" "$SKILLS_DIR/zh-en-academic"
  echo "   copied: zh-en-academic (custom)"
fi

echo
echo "Done. Restart Claude Code or run /reload-plugins to refresh the skill registry."
echo "Skills installed at: $SKILLS_DIR"
