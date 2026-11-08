#!/usr/bin/env python3
"""Record the platform's post/video/ad ID for a campaign code.

    python3 scripts/set_post_id.py R7K9XM dQw4w9WgXcQ
    python3 scripts/set_post_id.py R7K9XM urn:li:share:7261234567890 --force

Codes are usually created before the post exists, so post_id starts as null.
Once the video or post is live, run this to fill it in. It edits
_data/campaign_codes.yml as text, so comments and layout are preserved, and
validates the result before writing. post_id never goes into URLs or UTMs, so
there is no need to rerun build_go.py; it is there for the campaign dashboard
to join platform views to codes. --force replaces an ID that is already set.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign_codes as cc  # noqa: E402


class SetPostIdError(Exception):
    pass


def set_post_id(text, code, post_id, force=False):
    """Return `text` with post_id set on the entry for `code`."""
    lines = text.splitlines(True)
    start_re = re.compile(r'^- code:\s*["\']?%s["\']?\s*$' % re.escape(code))
    start = next((i for i, line in enumerate(lines) if start_re.match(line)), None)
    if start is None:
        raise SetPostIdError("code %s is not in campaign_codes.yml" % code)
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].strip() and not lines[i].startswith(" ")), len(lines))

    entry = next(e for e in cc.parse_entries(text) if isinstance(e, dict) and e.get("code") == code)
    if entry.get("legacy"):
        raise SetPostIdError("%s is a legacy code; legacy entries don't carry post_id" % code)
    current = entry.get("post_id")
    if current is not None and current != post_id and not force:
        raise SetPostIdError("%s already has post_id %r; use --force to replace it" % (code, current))

    new_line = "  post_id: %s\n" % cc.yaml_scalar(post_id)
    for i in range(start, end):
        if re.match(r"^(- |  )post_id:", lines[i]):
            lines[i] = new_line
            break
    else:
        # Older entry without the key: put it after video_uid (or `to`).
        anchor = None
        for key in ("video_uid", "to"):
            anchor = next((i for i in range(start, end)
                           if re.match(r"^(- |  )%s:" % key, lines[i])), None)
            if anchor is not None:
                break
        if anchor is None:
            anchor = max(i for i in range(start, end) if lines[i].strip())
        if not lines[anchor].endswith("\n"):
            lines[anchor] += "\n"
        lines.insert(anchor + 1, new_line)
    return "".join(lines)


def main(argv=None, data_file=None, repo_root=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__)
    p.add_argument("code", help="the campaign code, e.g. R7K9XM")
    p.add_argument("post_id", help="the platform's ID for the post, video or ad")
    p.add_argument("--force", action="store_true", help="replace a post_id that is already set")
    args = p.parse_args(argv)
    data_file = data_file or cc.DATA_FILE
    repo_root = repo_root or cc.REPO_ROOT

    with open(data_file, encoding="utf-8") as f:
        text = f.read()
    code = args.code.strip().upper()
    try:
        new_text = set_post_id(text, code, args.post_id.strip(), force=args.force)
        entries = cc.parse_entries(new_text, data_file)
    except (SetPostIdError, cc.ValidationError, cc.yaml.YAMLError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 1
    entry = next(e for e in entries if isinstance(e, dict) and e.get("code") == code)
    errors, _ = cc.validate_entry(entry, repo_root=repo_root)
    if errors:
        for e in errors:
            print("ERROR: %s: %s" % (code, e), file=sys.stderr)
        return 1
    if new_text == text:
        print("%s already has post_id %s; nothing to do." % (code, entry["post_id"]))
        return 0
    with open(data_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)
    print("Set %s post_id to %s." % (code, entry["post_id"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
