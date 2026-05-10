# CLAUDE.md — writings repo

Public repo for finished blog posts. Pushed to `github.com/jamesypub/writings`.

Drafts and review history stay in `~/jycode/blog-*/`. Only allowlisted posts move from there to here.

## Publish workflow

```bash
cd ~/writings
python3 scripts/publish.py            # dry-run — prints what would change
python3 scripts/publish.py --apply    # copy latest V{N} + referenced images
git add -A
git commit -m "publish: <post-name> V<N>"
git push
```

The script picks up the latest `blog-source--V{N}.md` automatically. Older drafts are ignored.

## Allowlist rule

`scripts/publish.py` has a hardcoded `ALLOWLIST` at the top. Nothing publishes unless it's listed there. To publish a new blog, add an entry — do not bypass the allowlist.

Current allowlist:
- `~/jycode/blog-agent-orchestration-architecture` → `posts/agent-orchestration-patterns/`

Only `.md` and `.png/.jpg/.jpeg/.svg` files are permitted. `.docx`, `changes.md`, session memory, older `V{N}` files, and any other file type are rejected.

## Repo structure

```
writings/
├── README.md                                 # public index
├── CLAUDE.md                                 # this file
├── posts/
│   └── <post-slug>/
│       ├── README.md                         # the post (GitHub renders it)
│       └── images/                           # referenced PNGs
└── scripts/
    ├── publish.py                            # allowlist-gated copy tool
    └── README.md
```

## Publishing to Medium

1. Run the publish workflow above so the post is on GitHub.
2. Go to `https://medium.com/p/import`.
3. Paste the GitHub URL, e.g. `https://github.com/jamesypub/writings/blob/main/posts/agent-orchestration-patterns/README.md`.
4. Medium pulls the markdown and images; review formatting, then publish.

Images load from `raw.githubusercontent.com` automatically — no path rewriting needed.

## Git auth

Pushes authenticate as `jamesypub` via a stored PAT at `~/.git-credentials-jamesypub` (mode 600). The repo's `.git/config` overrides the inherited `gh` credential helper so the correct token is used. See memory file `reference_jamesypub_git_auth.md` if auth ever breaks.

## Rules

- Never copy files directly from `~/jycode/blog-*` into this repo — always use `publish.py`.
- Never commit `.docx`, drafts, `changes.md`, or anything outside the allowlist.
- Always `git commit` and `git push` when done (project rule from `~/jycode/CLAUDE.md`).
