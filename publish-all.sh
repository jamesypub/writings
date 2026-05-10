#!/usr/bin/env bash
#
# publish-all.sh -- one command to publish the latest allowlisted blog.
#
# Steps:
#   1. Run the allowlist-gated publish.py (copies latest V{N} + referenced images)
#   2. If there are changes: commit and push (triggers GitHub Pages rebuild)
#   3. Print the Medium import URLs so you can paste them into medium.com/p/import
#
# Usage:
#   ./publish-all.sh                # apply + push + print URLs
#   ./publish-all.sh --dry-run      # show what publish.py would do, no commit
#
# Requires: python3, git, curl (optional: for Pages build status check)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

# --- step 1: publish ---------------------------------------------------------
if [[ $DRY_RUN -eq 1 ]]; then
  echo ">>> dry-run: python3 scripts/publish.py"
  python3 scripts/publish.py
  echo ""
  echo "(dry-run stops here -- rerun without --dry-run to commit + push)"
  exit 0
fi

echo ">>> copying latest blog source into posts/"
python3 scripts/publish.py --apply

# --- step 2: commit + push if changed ----------------------------------------
if [[ -z "$(git status --porcelain)" ]]; then
  echo ""
  echo ">>> no changes detected -- already up to date"
else
  echo ""
  echo ">>> staging + committing"
  git add -A
  # Use the current latest version number in the commit message
  latest_md="$(git diff --cached --name-only | grep -E 'posts/.*/README\.md$' | head -1 || true)"
  version="$(python3 -c "
import re, pathlib
for p in sorted(pathlib.Path('$HOME/jycode/blog-agent-orchestration-architecture/Output').glob('blog-source--V*.md')):
    m = re.search(r'V(\d+)', p.name)
    if m: v = int(m.group(1))
print(v)
" 2>/dev/null || echo "unknown")"
  git commit -m "publish: agent-orchestration-patterns V${version}"

  echo ""
  echo ">>> pushing to origin"
  git push
fi

# --- step 3: print Medium import URLs ---------------------------------------
cat <<'EOF'

>>> To publish on Medium:

  1. Open: https://medium.com/p/import

  2. Paste one of these URLs (try GitHub first; if images don't load, use Pages):

     GitHub (rendered README):
       https://github.com/jamesypub/writings/blob/main/posts/agent-orchestration-patterns/README.md

     GitHub Pages (Jekyll-rendered):
       https://jamesypub.github.io/writings/posts/agent-orchestration-patterns/

  3. Click Import. Medium creates a DRAFT.
  4. Review, then click Publish on Medium.

GitHub Pages typically rebuilds within ~60 seconds of pushing.
EOF
