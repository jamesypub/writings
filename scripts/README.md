# Publish script

`publish.py` copies the latest version of each allowlisted internal blog into this public repo.

## Allowlist

Edit `ALLOWLIST` at the top of `publish.py`. Each entry pairs one internal source folder with one public post folder. **No folder can publish unless it's on this list.**

## Guarantees

- Only the latest `blog-source--V{N}.md` in each allowlisted folder is published.
- Only images the markdown actually references are copied.
- Only `.md` and `.png/.jpg/.jpeg/.svg` files are permitted — anything else aborts.
- Image paths must resolve inside the allowlisted source folder.
- `.docx`, `changes.md`, drafts, older `V{N}` files, and session memory are never read.

## Usage

```bash
# dry-run (default) -- prints what would be copied, touches nothing
python3 scripts/publish.py

# actually copy the files
python3 scripts/publish.py --apply

# then review and push
git status
git diff
git add -A && git commit -m "publish: <post> V<N>" && git push
```
