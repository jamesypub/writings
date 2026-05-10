# CLAUDE.md — writings repo

Public repo for finished blog posts. Pushed to `github.com/jamesypub/writings`. Rendered site at `jamesypub.github.io/writings`.

Drafts and review history stay in `~/jycode/blog-*/`. Only allowlisted posts move from there to here.

---

## Publishing an existing blog (routine case)

You've already set up the blog (it's in the allowlist). New version is ready in `~/jycode/blog-*/Output/blog-source--V{N}.md`.

```bash
cd ~/writings
./publish-all.sh --dry-run   # preview (optional)
./publish-all.sh             # apply + commit + push
```

The script:
1. Copies the latest `blog-source--V{N}.md` + referenced images from the allowlisted `jycode/` folder.
2. Injects Jekyll front matter (title, permalink) so Pages renders it cleanly.
3. Commits and pushes to GitHub.
4. Prints two URLs to paste into Medium.

GitHub Pages rebuilds in ~1 minute. The site is at:
- Homepage: https://jamesypub.github.io/writings/
- Each post: https://jamesypub.github.io/writings/posts/&lt;slug&gt;/

## Importing to Medium (one-time, after each publish)

1. Open `https://medium.com/p/import`
2. Paste the URL the script printed:
   `https://github.com/jamesypub/writings/blob/main/posts/<slug>/README.md`
3. Click **Import**. Medium creates a draft.
4. Fix the things Medium's importer drops (see checklist below).
5. Click **Publish** on Medium.

### Medium post-import checklist — do these BEFORE publishing

After import, in Medium's editor:

- [ ] **Add co-authors via Medium's "Add authors"** — links co-authors who are Medium users so they appear on the byline with profile chips (the italic byline line in the markdown is informational only; Medium needs this UI step for official co-author attribution)
- [ ] **Image captions** — check that figure captions render italic (importer occasionally styles them as body text)

Things that are now automatic (no longer need manual fixing):
- Title is preserved from the markdown H1.
- Byline text (`*By X and Y*`) imports as italic text directly below the title.
- Author credits at the end of the post — if you add a bio block at the bottom of the source markdown in `~/jycode/.../Output/blog-source--V{N}.md`, it flows through.

## Adding a NEW blog (the first time)

When you want to publish a different blog for the first time:

### 1. Confirm the source blog is ready
The source blog in `~/jycode/blog-*/` must have:
- An `Output/` folder containing `blog-source--V{N}.md` files
- Images referenced as `![alt](generated-diagrams/<name>.png)` or similar relative paths inside the blog folder

### 2. Add it to the allowlist
Edit `~/writings/scripts/publish.py` and add a new entry to `ALLOWLIST`:

```python
ALLOWLIST = [
    {
        "source_dir": HOME / "jycode/blog-agent-orchestration-architecture",
        "post_dir":   REPO_ROOT / "posts/agent-orchestration-patterns",
        "title":      "Building multi-agent applications: orchestration patterns",
    },
    # ← Add your new blog here, same shape:
    {
        "source_dir": HOME / "jycode/blog-<your-blog-folder>",
        "post_dir":   REPO_ROOT / "posts/<your-post-slug>",
        "title":      "Your Blog Title Here",
    },
]
```

Notes:
- `source_dir` — absolute path to the private jycode blog folder
- `post_dir` — where it'll land in this public repo; pick a URL-friendly slug
- `title` — used in Jekyll front matter and as the Pages page title

### 3. Update the homepage index
Edit `~/writings/index.md` and add the new post to the list:

```markdown
- **[Your Blog Title Here](posts/<your-post-slug>/)**
  One-sentence summary of the post.
```

Also add it to `~/writings/README.md` (the GitHub repo landing page), same format.

### 4. Publish
```bash
cd ~/writings
./publish-all.sh --dry-run   # sanity-check what will be copied
./publish-all.sh             # apply + commit + push
```

### 5. Import to Medium
Same Medium import flow as above, with the new URL the script prints.

---

## Safety / allowlist rules

`scripts/publish.py` has a hardcoded `ALLOWLIST` at the top. **Nothing publishes unless it's listed there.** To publish a new blog, add an entry — do not bypass the allowlist.

Only `.md` and `.png/.jpg/.jpeg/.svg` files are permitted. `.docx`, `changes.md`, session memory, older `V{N}` files, and any other file type are rejected — the script aborts if it sees one.

**Current allowlist:**
- `~/jycode/blog-agent-orchestration-architecture` → `posts/agent-orchestration-patterns/`

## Repo structure

```
writings/
├── README.md                             # GitHub landing page
├── CLAUDE.md                             # this file
├── _config.yml                           # Jekyll / GitHub Pages config
├── index.md                              # Pages homepage (rendered at jamesypub.github.io/writings/)
├── publish-all.sh                        # one-command publish wrapper
├── posts/
│   └── <post-slug>/
│       ├── README.md                     # the post (Jekyll front matter + markdown)
│       └── images/                       # referenced PNGs
└── scripts/
    ├── publish.py                        # allowlist-gated copy tool
    └── README.md
```

## Git auth

Pushes authenticate as `jamesypub` via a stored PAT at `~/.git-credentials-jamesypub` (mode 600). The repo's `.git/config` has a URL-scoped helper override so the correct token is used instead of the `gh` CLI's (which is logged in as `jamesyangoc`). See memory file `reference_jamesypub_git_auth.md` if auth ever breaks.

## Rules

- Never copy files directly from `~/jycode/blog-*` into this repo — always use `publish.py`.
- Never commit `.docx`, drafts, `changes.md`, or anything outside the allowlist.
- Always `git commit` and `git push` when done (project rule from `~/jycode/CLAUDE.md`).

## Published posts

| Version | Date | Medium URL |
|---|---|---|
| V41 of agent-orchestration-patterns | 2026-05-10 | https://medium.com/p/e5a17d27c404 |
