#!/usr/bin/env python3
"""One-time migration: copy the hand-written _go/*.md codes into the YAML.

    python3 scripts/migrate_existing_codes.py

Reads each existing _go/<CODE>.md front matter and appends a `legacy: true`
entry to _data/campaign_codes.yml with every field copied exactly as it is.
Fields a file left out stay null, so the redirect layout's defaults keep
applying and GA history stays continuous. `created` is the date git first
added the file. Codes already in the YAML are skipped, so re-running is safe.

Run scripts/build_go.py afterwards. This script can be deleted once the
migration has merged.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign_codes as cc  # noqa: E402

# Front-matter keys the hand-written files used (permalink is regenerated).
COPIED = ["note", "description", "to", "utm_source", "utm_medium", "utm_campaign",
          "utm_content", "utm_term"]


def read_front_matter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    parts = text.split("---", 2)
    if not text.startswith("---") or len(parts) < 3:
        raise SystemExit("%s has no front matter" % path)
    if parts[2].strip():
        raise SystemExit("%s has body content after the front matter; migrate it by hand" % path)
    return cc.yaml.safe_load(parts[1]) or {}


def git_created(path, repo_root):
    out = subprocess.check_output(
        ["git", "log", "--diff-filter=A", "--follow", "--format=%as", "--", path],
        cwd=repo_root, universal_newlines=True).split()
    if not out:
        raise SystemExit("%s is not in git history; can't determine created" % path)
    return cc.as_date(out[-1])  # oldest add


def legacy_entry(path, repo_root):
    code = os.path.splitext(os.path.basename(path))[0]
    fm = read_front_matter(path)
    if fm.get("permalink") != "/go/%s/" % code:
        raise SystemExit("%s: permalink %r doesn't match the code" % (path, fm.get("permalink")))
    unknown = sorted(set(fm) - set(COPIED) - {"permalink"})
    if unknown:
        raise SystemExit("%s: don't know how to migrate field(s) %s" % (path, ", ".join(unknown)))
    values = {k: fm.get(k) for k in COPIED}
    return cc.full_entry(code=code, created=git_created(path, repo_root), legacy=True, **values)


def main(go_dir=None, data_file=None, repo_root=None):
    go_dir = go_dir or cc.GO_DIR
    data_file = data_file or cc.DATA_FILE
    repo_root = repo_root or cc.REPO_ROOT

    existing = {e.get("code") for e in cc.load_entries(data_file) if isinstance(e, dict)}
    names = sorted(n for n in os.listdir(go_dir) if n.endswith(".md"))
    entries = []
    for name in names:
        path = os.path.join(go_dir, name)
        entry = legacy_entry(path, repo_root)
        if entry["code"] in existing:
            print("skip %s (already in %s)" % (entry["code"], os.path.relpath(data_file)))
            continue
        entries.append(entry)

    if not entries:
        print("Nothing to migrate.")
        return 0

    if os.path.exists(data_file):
        with open(data_file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = cc.DATA_HEADER
    if not text.endswith("\n"):
        text += "\n"
    for entry in entries:
        text += "\n" + cc.entry_to_yaml(entry)

    errors, warnings = cc.validate_entries(cc.parse_entries(text), repo_root=repo_root)
    for w in warnings:
        print("WARNING: %s" % w)
    if errors:
        for e in errors:
            print("ERROR: %s" % e, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    for entry in entries:
        print("migrated %s (created %s)" % (entry["code"], entry["created"]))
    print("Wrote %d legacy entries to %s. Next: python3 scripts/build_go.py"
          % (len(entries), os.path.relpath(data_file)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
