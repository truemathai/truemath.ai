#!/usr/bin/env python3
"""Create campaign codes and append them to _data/campaign_codes.yml.

Single code:

    python3 scripts/new_code.py \\
      --series cleared-for-exactness \\
      --episode ep1-weight-and-balance \\
      --platform youtube \\
      --placement description \\
      --to /series/cleared-for-exactness#weight-and-balance \\
      --note "CfE Ep1 YouTube description link"

Batch (one code per CSV row; all-or-nothing):

    python3 scripts/new_code.py --batch campaign_batches/cfe-launch.csv

The batch writes <input>.codes.csv next to the CSV with every new code and URL.
Afterwards run python3 scripts/build_go.py to regenerate _go/.
"""

import argparse
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign_codes as cc  # noqa: E402

BATCH_REQUIRED = ["series", "episode", "platform", "placement", "to", "video_uid", "note"]
BATCH_OPTIONAL = ["description", "abbr", "utm_term", "owner", "destination_type",
                  "expires", "qr_generated"]
OUTPUT_COLUMNS = ["code", "url", "utm_content", "series", "episode", "platform",
                  "placement", "note"]


def _clean(value):
    if value is None:
        return None
    value = value.strip()
    return value or None


def parse_qr(value):
    value = _clean(value) if isinstance(value, str) or value is None else value
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False
    return value  # a path under campaign_assets/


def parse_date(value):
    value = _clean(value)
    if value is None:
        return None
    return cc.as_date(value) or value  # leave bad input for validation to report


def build_entry(code, series, episode, platform, placement, to, note=None,
                video_uid=None, description=None, abbr=None, utm_term=None,
                owner=None, destination_type=None, expires=None, qr_generated=None,
                today=None):
    series, episode, platform, placement = (_clean(series), _clean(episode),
                                            _clean(platform), _clean(placement))
    entry = cc.full_entry(
        code=code,
        series=series,
        episode=episode,
        platform=platform,
        placement=placement,
        to=_clean(to),
        video_uid=_clean(video_uid),
        utm_term=_clean(utm_term),
        note=_clean(note),
        created=today or datetime.date.today(),
        description=_clean(description),
        legacy=False,
        expires=parse_date(expires),
        owner=_clean(owner) or "bill",
        destination_type=_clean(destination_type) or "landing-page",
        qr_generated=parse_qr(qr_generated),
    )
    if series and platform in cc.PLATFORM_MEDIUM and placement:
        entry.update(cc.derive_utm(series, episode, platform, placement, abbr=_clean(abbr)))
    else:
        # Leave UTM fields empty; validation reports the underlying problem.
        entry.update({"utm_source": platform, "utm_medium": None,
                      "utm_campaign": series, "utm_content": None})
    return entry


def read_data_text(path):
    if not os.path.exists(path):
        return cc.DATA_HEADER
    with open(path, encoding="utf-8") as f:
        return f.read()


def append_entries(text, entries):
    if text and not text.endswith("\n"):
        text += "\n"
    for entry in entries:
        text += "\n" + cc.entry_to_yaml(entry)
    return text


def commit(entries, data_file, repo_root, dry_run):
    """Validate the data file with `entries` appended, then write it.

    Returns a list of errors (empty on success).
    """
    new_text = append_entries(read_data_text(data_file), entries)
    try:
        all_entries = cc.parse_entries(new_text, data_file)
    except (cc.ValidationError, cc.yaml.YAMLError) as exc:
        return ["could not parse %s: %s" % (data_file, exc)]
    errors, warnings = cc.validate_entries(all_entries, repo_root=repo_root)
    for w in warnings:
        print("WARNING: %s" % w)
    if errors:
        return errors
    if not dry_run:
        with open(data_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
    return []


def run_single(args, data_file, repo_root):
    existing = {e.get("code") for e in cc.load_entries(data_file) if isinstance(e, dict)}
    entry = build_entry(
        cc.new_unique_code(existing), args.series, args.episode, args.platform,
        args.placement, args.to, note=args.note, video_uid=args.video_uid,
        description=args.description, abbr=args.abbr, utm_term=args.utm_term,
        owner=args.owner, destination_type=args.destination_type,
        expires=args.expires, qr_generated=args.qr)
    errors = commit([entry], data_file, repo_root, args.dry_run)
    if errors:
        for e in errors:
            print("ERROR: %s" % e, file=sys.stderr)
        return 1
    if args.dry_run:
        print("Dry run, nothing written. Entry would be:\n")
        print(cc.entry_to_yaml(entry))
    print("%s  %s" % (entry["code"], cc.go_url(entry["code"])))
    if not args.dry_run:
        print("Added to %s. Next: python3 scripts/build_go.py" % os.path.relpath(data_file))
    return 0


def run_batch(path, data_file, repo_root, dry_run, today=None):
    out_path = os.path.splitext(path)[0] + ".codes.csv"
    if not dry_run and os.path.exists(out_path):
        print("ERROR: %s already exists; move it aside so its codes aren't lost." % out_path,
              file=sys.stderr)
        return 1
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = [c.strip() for c in (reader.fieldnames or [])]
        missing = [c for c in BATCH_REQUIRED if c not in columns]
        unknown = [c for c in columns if c not in BATCH_REQUIRED + BATCH_OPTIONAL]
        if missing or unknown:
            if missing:
                print("ERROR: %s is missing column(s): %s" % (path, ", ".join(missing)),
                      file=sys.stderr)
            if unknown:
                print("ERROR: %s has unknown column(s): %s" % (path, ", ".join(unknown)),
                      file=sys.stderr)
            return 1
        rows = [{k.strip(): v for k, v in row.items() if k is not None} for row in reader]
    if not rows:
        print("ERROR: %s has no rows" % path, file=sys.stderr)
        return 1

    taken = {e.get("code") for e in cc.load_entries(data_file) if isinstance(e, dict)}
    entries, errors = [], []
    for n, row in enumerate(rows, start=2):  # row 1 is the header
        code = cc.new_unique_code(taken)
        taken.add(code)
        kwargs = {k: row.get(k) for k in BATCH_OPTIONAL}
        entry = build_entry(code, row.get("series"), row.get("episode"), row.get("platform"),
                            row.get("placement"), row.get("to"), note=row.get("note"),
                            video_uid=row.get("video_uid"), today=today, **kwargs)
        row_errors, _ = cc.validate_entry(entry, repo_root=repo_root)
        errors += ["row %d: %s" % (n, m) for m in row_errors]
        entries.append(entry)
    if not errors:
        errors = commit(entries, data_file, repo_root, dry_run)
    if errors:
        for e in errors:
            print("ERROR: %s" % e, file=sys.stderr)
        print("Nothing written.", file=sys.stderr)
        return 1

    for e in entries:
        print("%s  %s  %s" % (e["code"], cc.go_url(e["code"]), e["utm_content"]))
    if dry_run:
        print("Dry run: %d codes validated, nothing written." % len(entries))
        return 0
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(OUTPUT_COLUMNS)
        for e in entries:
            writer.writerow([e["code"], cc.go_url(e["code"])] +
                            [e.get(k) or "" for k in OUTPUT_COLUMNS[2:]])
    print("Added %d codes to %s and wrote %s. Next: python3 scripts/build_go.py"
          % (len(entries), os.path.relpath(data_file), out_path))
    return 0


def main(argv=None, data_file=None, repo_root=None):
    p = argparse.ArgumentParser(
        description="Create campaign codes in _data/campaign_codes.yml.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("--batch", metavar="CSV", help="create one code per row of a CSV file")
    p.add_argument("--series", help="series slug, e.g. cleared-for-exactness (utm_campaign)")
    p.add_argument("--episode", help="episode slug, e.g. ep1-weight-and-balance; omit for series-level links")
    p.add_argument("--platform", choices=cc.PLATFORMS, help="where the code is used (utm_source)")
    p.add_argument("--placement", choices=cc.PLACEMENTS, help="where on the platform")
    p.add_argument("--to", help="destination: site path (/x, /x#section) or full http(s) URL")
    p.add_argument("--note", help="short internal label (never in URLs or GA)")
    p.add_argument("--video-uid", help="Cloudflare Stream UID, appended to the destination as ?v=")
    p.add_argument("--description", help="fuller internal detail")
    p.add_argument("--abbr", help="override the series abbreviation used in utm_content")
    p.add_argument("--utm-term", help="optional utm_term")
    p.add_argument("--owner", default="bill", help="who requested the code (default: bill)")
    p.add_argument("--destination-type", default="landing-page", choices=cc.DESTINATION_TYPES,
                   help="what the visitor lands on (default: landing-page)")
    p.add_argument("--qr", nargs="?", const="true", default=None, metavar="PATH",
                   help="mark that a QR asset exists, or give its path under campaign_assets/")
    p.add_argument("--expires", help="date to retire the code, YYYY-MM-DD")
    p.add_argument("--dry-run", action="store_true", help="validate and print; write nothing")
    args = p.parse_args(argv)

    data_file = data_file or cc.DATA_FILE
    repo_root = repo_root or cc.REPO_ROOT
    if args.batch:
        return run_batch(args.batch, data_file, repo_root, args.dry_run)
    missing = [flag for flag, v in (("--series", args.series), ("--platform", args.platform),
                                    ("--placement", args.placement), ("--to", args.to)) if not v]
    if missing:
        p.error("missing required option(s): %s (or use --batch)" % ", ".join(missing))
    return run_single(args, data_file, repo_root)


if __name__ == "__main__":
    sys.exit(main())
