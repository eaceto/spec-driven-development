#!/bin/sh
# Install the spec-driven development skills into a project.
#
#   ./install.sh <project-dir>          copy the skills into the project
#   ./install.sh <project-dir> --link   symlink them instead (for working on the skills in this repository)
#
# What it does:
#   1. Copies skills/sdd-*/ into <project>/.agents/skills/ and <project>/.claude/skills/.
#   2. Bundles specs/templates/ into the installed sdd-init so it can create specs/ in a project that has none.
#   3. Writes the version from VERSION into sdd_version in <project>/specs/constitution.md, if that file exists.
#   4. Creates <project>/CLAUDE.md pointing to AGENTS.md if the project has no CLAUDE.md.
set -eu

usage() { echo "usage: $0 <project-dir> [--link]" >&2; exit 2; }
[ $# -ge 1 ] || usage
TARGET=$1; shift
LINK=0
for arg in "$@"; do
  case "$arg" in
    --link) LINK=1 ;;
    *) usage ;;
  esac
done

HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/skills"
TEMPLATES="$HERE/specs/templates"
VERSION=$(tr -d '[:space:]' < "$HERE/VERSION")

[ -d "$TARGET" ] || { echo "no such directory: $TARGET" >&2; exit 1; }
TARGET=$(cd "$TARGET" && pwd)

# Where agents look for skills. Add a location here, nowhere else.
DESTS=".agents/skills .claude/skills"

installed=""
for dest in $DESTS; do
  mkdir -p "$TARGET/$dest"
  for skill in "$SRC"/sdd-*/; do
    name=$(basename "$skill")
    rm -rf "$TARGET/$dest/$name"
    if [ "$LINK" = 1 ]; then
      # Relative link from <target>/<dest>/ back to skills/ in this checkout.
      if [ "$TARGET" = "$HERE" ]; then
        ln -s "../../skills/$name" "$TARGET/$dest/$name"
      else
        ln -s "$SRC/$name" "$TARGET/$dest/$name"
      fi
    else
      cp -RL "$skill" "$TARGET/$dest/$name"
      if [ "$name" = "sdd-init" ]; then
        rm -rf "$TARGET/$dest/$name/templates"
        cp -RL "$TEMPLATES" "$TARGET/$dest/$name/templates"
      fi
    fi
    installed="$installed $name"
  done
done

CONST="$TARGET/specs/constitution.md"
if [ -f "$CONST" ]; then
  tmp=$(mktemp)
  if grep -q '^sdd_version:' "$CONST"; then
    sed "s/^sdd_version:.*/sdd_version: $VERSION/" "$CONST" > "$tmp"
  else
    awk -v v="$VERSION" 'NR==1 && $0=="---" {print; print "sdd_version: " v; next} {print}' "$CONST" > "$tmp"
  fi
  mv "$tmp" "$CONST"
  echo "constitution: sdd_version set to $VERSION"
else
  echo "constitution: none yet; sdd-init will write it with sdd_version $VERSION"
fi

if [ ! -f "$TARGET/CLAUDE.md" ]; then
  printf 'Read `AGENTS.md` and follow it. It holds the loading rule and the lifecycle rules for this repository.\n' > "$TARGET/CLAUDE.md"
  echo "CLAUDE.md: created, pointing to AGENTS.md"
fi

mode=copied; [ "$LINK" = 1 ] && mode=linked
echo "skills $mode into $TARGET: $(echo $installed | tr ' ' '\n' | sort -u | tr '\n' ' ')"
echo "locations: $DESTS"
echo "next: in your agent, run sdd-init (new project) or sdd-new (project already initialised)"
