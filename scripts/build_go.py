#!/usr/bin/env python3
"""Regenerate _go/*.md redirect files from _data/campaign_codes.yml.

    python3 scripts/build_go.py           # validate, then rewrite _go/
    python3 scripts/build_go.py --check   # validate and compare; write nothing

The YAML file is the only place campaign codes are edited. Every file in _go/
is generated: this script deletes them all and writes one per entry. --check
exits non-zero if any entry is invalid or _go/ doesn't match the YAML; run it
before opening a pull request. Warnings (expired codes, shared utm_content,
possible personal data) are printed but don't fail the build.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign_codes as cc  # noqa: E402


def expected_files(entries):
    return {"%s.md" % e["code"]: cc.render_go_file(e) for e in entries}


def current_files(go_dir):
    if not os.path.isdir(go_dir):
        return {}
    out = {}
    for name in sorted(os.listdir(go_dir)):
        path = os.path.join(go_dir, name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8", newline="") as f:
                out[name] = f.read()
    return out


def diff_files(expected, actual):
    """Return a list of human-readable differences (empty when in sync)."""
    problems = []
    for name in sorted(set(expected) - set(actual)):
        problems.append("missing   _go/%s" % name)
    for name in sorted(set(actual) - set(expected)):
        problems.append("extra     _go/%s (not in campaign_codes.yml)" % name)
    for name in sorted(set(expected) & set(actual)):
        if expected[name] != actual[name]:
            problems.append("outdated  _go/%s" % name)
    return problems


def main(argv=None, data_file=None, go_dir=None, repo_root=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="write nothing; fail if _go/ doesn't match the YAML")
    args = parser.parse_args(argv)
    data_file = data_file or cc.DATA_FILE
    go_dir = go_dir or cc.GO_DIR
    repo_root = repo_root or cc.REPO_ROOT

    try:
        entries = cc.load_entries(data_file)
    except (cc.ValidationError, cc.yaml.YAMLError) as exc:
        print("ERROR: could not read %s: %s" % (data_file, exc), file=sys.stderr)
        return 1

    errors, warnings = cc.validate_entries(entries, repo_root=repo_root)
    for w in warnings:
        print("WARNING: %s" % w)
    if errors:
        for e in errors:
            print("ERROR: %s" % e, file=sys.stderr)
        print("%d error(s) in %s; nothing written." % (len(errors), data_file),
              file=sys.stderr)
        return 1

    expected = expected_files(entries)
    legacy = sum(1 for e in entries if e.get("legacy"))

    if args.check:
        problems = diff_files(expected, current_files(go_dir))
        if problems:
            for p in problems:
                print("ERROR: %s" % p, file=sys.stderr)
            print("_go/ is out of date: run python3 scripts/build_go.py and commit the result.",
                  file=sys.stderr)
            return 1
        print("OK: %d codes (%d legacy), _go/ matches campaign_codes.yml, %d warning(s)."
              % (len(expected), legacy, len(warnings)))
        return 0

    os.makedirs(go_dir, exist_ok=True)
    for name in os.listdir(go_dir):
        path = os.path.join(go_dir, name)
        if os.path.isfile(path):
            os.remove(path)
    for name, content in sorted(expected.items()):
        with open(os.path.join(go_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
    print("Generated %d redirect files in _go/ (%d legacy), %d warning(s)."
          % (len(expected), legacy, len(warnings)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
