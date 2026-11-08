"""Shared helpers for the /go/ campaign code system.

Used by new_code.py, build_go.py and migrate_existing_codes.py. Covers code
generation, UTM derivation, validation of _data/campaign_codes.yml entries, and
a small YAML emitter that writes entries as text (so new_code.py can append to
the data file without disturbing its comments or layout).

Python 3.8+, PyYAML only.
"""

import datetime
import json
import os
import re
import secrets
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - depends on the machine
    sys.exit("PyYAML is required: python3 -m pip install --user pyyaml")


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(REPO_ROOT, "_data", "campaign_codes.yml")
GO_DIR = os.path.join(REPO_ROOT, "_go")

SITE_HOST = "truemath.ai"

# Crockford Base32: digits plus uppercase letters minus I, L, O, U.
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
CODE_LENGTH = 6
CODE_RE = re.compile(r"^[%s]{%d}$" % (CROCKFORD, CODE_LENGTH))

PLATFORMS = [
    "youtube", "linkedin", "facebook", "tiktok", "instagram",
    "qr", "email", "podcast", "trade-media",
]
PLACEMENTS = [
    "description", "pinned-comment", "end-screen", "bio-link", "post",
    "story", "group-post", "show-notes", "print", "slide", "ad",
]
DESTINATION_TYPES = [
    "landing-page", "video", "playground", "domain-signup", "series-page",
    "external",
]
PLATFORM_MEDIUM = {
    "youtube": "video",
    "tiktok": "video",
    "instagram": "video",
    "linkedin": "social",
    "facebook": "social",
    "qr": "qr",
    "email": "email",
    "podcast": "podcast",
    "trade-media": "referral",
}

# Every key an entry may carry, in the order they are written to the data file.
FIELDS = [
    "code", "campaign", "series", "episode", "platform", "placement", "paid",
    "to", "video_uid", "post_id", "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "note", "created", "description", "legacy", "expires", "owner",
    "destination_type", "qr_generated",
]
UTM_FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]
REQUIRED_UTM = ["utm_source", "utm_medium", "utm_campaign", "utm_content"]
# Added after the Nov 5 spec; only non-legacy entries carry them.
NON_LEGACY_FIELDS = ["campaign", "paid", "post_id"]

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VIDEO_UID_RE = re.compile(r"^[0-9a-f]{32}$")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
URL_RE = re.compile(r"^https?://[^\s/]+\S*$")
QR_DIR = "campaign_assets/"

# Heuristics for the "no PII in utm_* / note / description" rule. These only
# warn; nothing can prove a value is free of personal data.
EMAIL_RE = re.compile(r"[^\s@]+@[^\s@]+\.[a-z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:\+?\d[\s().-]?){10,}")


class ValidationError(Exception):
    pass


# --------------------------------------------------------------------------
# Codes and UTM derivation
# --------------------------------------------------------------------------

def random_code():
    return "".join(secrets.choice(CROCKFORD) for _ in range(CODE_LENGTH))


def new_unique_code(existing):
    """Return a random code not in `existing` (a set); regenerate on collision."""
    while True:
        code = random_code()
        if code not in existing:
            return code


def series_abbr(series):
    """cleared-for-exactness -> cfe, the-cap-table -> tct, dana -> dana."""
    words = [w for w in series.split("-") if w]
    if len(words) == 1:
        return words[0]
    return "".join(w[0] for w in words)


def episode_part(episode):
    """ep1-weight-and-balance -> ep1; no episode (series-level link) -> series."""
    if not episode:
        return "series"
    return episode.split("-")[0]


def utm_campaign_for(campaign, series):
    """The one place utm_campaign is derived: <campaign>-<series>.

    exactly + cleared-for-exactness -> exactly-cleared-for-exactness.
    """
    return "%s-%s" % (campaign, series)


def utm_medium_for(platform, paid=False):
    """Medium for a platform; paid placements get a "paid-" prefix so GA4's
    default channel grouping files them under the paid channels."""
    medium = PLATFORM_MEDIUM[platform]
    return "paid-" + medium if paid else medium


def derive_utm(campaign, series, episode, platform, placement, paid=False, abbr=None):
    if platform not in PLATFORM_MEDIUM:
        raise ValidationError(
            "platform %r must be one of: %s" % (platform, ", ".join(PLATFORMS)))
    content = "-".join([abbr or series_abbr(series), episode_part(episode),
                        platform, placement])
    return {
        "utm_source": platform,
        "utm_medium": utm_medium_for(platform, paid),
        "utm_campaign": utm_campaign_for(campaign, series),
        "utm_content": content,
    }


def go_url(code):
    return "https://%s/go/%s" % (SITE_HOST, code)


def destination_with_video(to, video_uid):
    """Add ?v=<uid> (or &v=) to `to`, before any #section."""
    if not video_uid:
        return to
    main, hash_, frag = to.partition("#")
    sep = "&" if "?" in main else "?"
    return main + sep + "v=" + video_uid + hash_ + frag


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_entries(path=DATA_FILE):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return parse_entries(f.read(), path)


def parse_entries(text, label="campaign_codes.yml"):
    data = yaml.safe_load(text)
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValidationError("%s must be a YAML list of entries" % label)
    return data


def as_date(value):
    """Return a datetime.date for a YAML date or an ISO string, else None."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def _blank(value):
    return value is None or (isinstance(value, str) and value.strip() == "")


def validate_entry(entry, repo_root=REPO_ROOT, today=None):
    """Return (errors, warnings) for one entry. Does not check uniqueness."""
    errors, warnings = [], []
    if not isinstance(entry, dict):
        return ["entry is not a mapping: %r" % (entry,)], warnings

    unknown = sorted(set(entry) - set(FIELDS))
    if unknown:
        errors.append("unknown field(s): %s" % ", ".join(unknown))

    code = entry.get("code")
    legacy = entry.get("legacy", False)
    if not isinstance(legacy, bool):
        errors.append("legacy must be true or false")
        legacy = False

    if not isinstance(code, str) or not CODE_RE.match(code):
        errors.append("code %r must be 6 uppercase Crockford Base32 characters (%s)"
                      % (code, CROCKFORD))

    # to
    to = entry.get("to")
    if _blank(to) or not isinstance(to, str):
        errors.append("to is required")
    elif re.search(r"\s", to):
        errors.append("to %r must not contain spaces" % to)
    elif to.startswith("/"):
        if to.startswith("//"):
            errors.append("to %r: a site path must start with a single /" % to)
    elif not URL_RE.match(to):
        errors.append("to %r must be a site path starting with / or a full http(s) URL" % to)

    # video_uid
    video_uid = entry.get("video_uid")
    if video_uid is not None:
        if not isinstance(video_uid, str) or not VIDEO_UID_RE.match(video_uid):
            errors.append("video_uid %r must be a 32-character lowercase hex Cloudflare Stream UID"
                          % (video_uid,))
        if isinstance(to, str) and re.search(r"[?&]v=", to.partition("#")[0]):
            errors.append("to %r already carries ?v=; set it via video_uid only" % to)

    # Series / episode / platform / placement
    series = entry.get("series")
    campaign = entry.get("campaign")
    if legacy:
        for field in NON_LEGACY_FIELDS:
            if entry.get(field) not in (None, False):
                errors.append("%s is not used on legacy entries" % field)
    else:
        if _blank(campaign):
            errors.append("campaign is required (e.g. exactly)")
        if _blank(series):
            errors.append("series is required")
        for field in ("platform", "placement"):
            if _blank(entry.get(field)):
                errors.append("%s is required" % field)
    for field in ("campaign", "series", "episode"):
        value = entry.get(field)
        if value is not None and not (isinstance(value, str) and SLUG_RE.match(value)):
            errors.append("%s %r must be a lowercase slug (letters, digits, hyphens)"
                          % (field, value))
    for field, allowed in (("platform", PLATFORMS), ("placement", PLACEMENTS)):
        value = entry.get(field)
        if value is not None and value not in allowed:
            errors.append("%s %r must be one of: %s" % (field, value, ", ".join(allowed)))

    # UTM values
    for field in UTM_FIELDS:
        value = entry.get(field)
        if value is not None and not isinstance(value, str):
            errors.append("%s must be a string, got %r" % (field, value))
    if not legacy:
        for field in REQUIRED_UTM:
            if _blank(entry.get(field)):
                errors.append("%s is required" % field)
        for field in UTM_FIELDS:
            value = entry.get(field)
            if isinstance(value, str) and value:
                if value != value.lower() or re.search(r"\s", value):
                    errors.append("%s %r must be lowercase with no spaces (use hyphens)"
                                  % (field, value))
        utm_campaign = entry.get("utm_campaign")
        if (isinstance(campaign, str) and campaign and isinstance(series, str) and series
                and isinstance(utm_campaign, str) and utm_campaign):
            expected = utm_campaign_for(campaign, series)
            if utm_campaign != expected:
                errors.append("utm_campaign %r must be %r (campaign-series)"
                              % (utm_campaign, expected))

    # paid / post_id
    paid = entry.get("paid", False)
    if paid is not None and not isinstance(paid, bool):
        errors.append("paid must be true or false")
    post_id = entry.get("post_id")
    if post_id is not None:
        if not isinstance(post_id, str):
            errors.append("post_id %r must be a string (quote numeric IDs)" % (post_id,))
        elif not post_id or re.search(r"\s", post_id):
            errors.append("post_id %r must be non-empty with no whitespace" % post_id)
        elif entry.get("platform") == "youtube" and not YOUTUBE_ID_RE.match(post_id):
            errors.append("post_id %r must be an 11-character YouTube video ID" % post_id)

    # PII heuristics (warnings only)
    for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content",
                  "utm_term", "note", "description"):
        value = entry.get(field)
        if isinstance(value, str) and (EMAIL_RE.search(value) or PHONE_RE.search(value)):
            warnings.append("%s looks like it contains an email address or phone number; "
                            "the repo is public, keep personal data out" % field)

    # Dates
    created = as_date(entry.get("created"))
    if created is None:
        errors.append("created %r must be a valid date (YYYY-MM-DD)" % (entry.get("created"),))
    expires_raw = entry.get("expires")
    if expires_raw is not None:
        expires = as_date(expires_raw)
        if expires is None:
            errors.append("expires %r must be a valid date (YYYY-MM-DD)" % (expires_raw,))
        else:
            if created is not None and expires < created:
                errors.append("expires %s is before created %s" % (expires, created))
            if expires <= (today or datetime.date.today()):
                warnings.append("expired on %s (still redirects; retire or extend it)" % expires)

    # Owner / destination type
    owner = entry.get("owner")
    if owner is not None and not (isinstance(owner, str) and SLUG_RE.match(owner)):
        errors.append("owner %r must be a lowercase slug (letters, digits, hyphens)" % (owner,))
    dtype = entry.get("destination_type")
    if dtype is not None and dtype not in DESTINATION_TYPES:
        errors.append("destination_type %r must be one of: %s"
                      % (dtype, ", ".join(DESTINATION_TYPES)))

    # QR asset
    qr = entry.get("qr_generated", False)
    if qr is None or isinstance(qr, bool):
        pass
    elif isinstance(qr, str):
        norm = qr.replace("\\", "/")
        if (not norm.startswith(QR_DIR) or norm.startswith("/")
                or ".." in norm.split("/")):
            errors.append("qr_generated %r must be true, false, or a relative path under %s"
                          % (qr, QR_DIR))
        elif not os.path.isfile(os.path.join(repo_root, norm)):
            errors.append("qr_generated file %s does not exist" % qr)
    else:
        errors.append("qr_generated must be true, false, or a path under %s" % QR_DIR)

    for field in ("note", "description"):
        value = entry.get(field)
        if value is not None and not isinstance(value, str):
            errors.append("%s must be a string" % field)

    return errors, warnings


def validate_entries(entries, repo_root=REPO_ROOT, today=None):
    """Validate every entry plus cross-entry rules.

    Returns (errors, warnings), each a list of "CODE: message" strings.
    """
    errors, warnings = [], []
    seen_codes = {}
    seen_content = {}
    for i, entry in enumerate(entries):
        label = entry.get("code") if isinstance(entry, dict) else None
        label = label or "entry #%d" % (i + 1)
        e, w = validate_entry(entry, repo_root=repo_root, today=today)
        errors += ["%s: %s" % (label, m) for m in e]
        warnings += ["%s: %s" % (label, m) for m in w]
        if not isinstance(entry, dict):
            continue
        code = entry.get("code")
        if isinstance(code, str):
            if code in seen_codes:
                errors.append("%s: duplicate code (also entry #%d)" % (code, seen_codes[code]))
            else:
                seen_codes[code] = i + 1
        content = entry.get("utm_content")
        if isinstance(content, str) and content:
            seen_content.setdefault(content, []).append(label)
    for content, codes in sorted(seen_content.items()):
        if len(codes) > 1:
            warnings.append("%s: share utm_content %r, so GA reports them as one row"
                            % (", ".join(codes), content))
    return errors, warnings


# --------------------------------------------------------------------------
# YAML text emitter
# --------------------------------------------------------------------------

def yaml_scalar(value, quote=False):
    """Render one scalar as YAML text that safe_load reads back unchanged."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return repr(value)
    text = str(value)
    if not quote and text and re.match(r"^[A-Za-z0-9/][A-Za-z0-9_./?=&%+:#-]*$", text):
        try:
            if yaml.safe_load(text) == text:
                return text
        except yaml.YAMLError:
            pass
    # JSON string syntax is valid YAML double-quoted syntax.
    return json.dumps(text, ensure_ascii=False)


def entry_to_yaml(entry):
    """Render an entry as a YAML list item, keys in FIELDS order."""
    lines = []
    keys = [k for k in FIELDS if k in entry] + [k for k in entry if k not in FIELDS]
    for i, key in enumerate(keys):
        prefix = "- " if i == 0 else "  "
        quote = key in ("note", "description")
        lines.append("%s%s: %s" % (prefix, key, yaml_scalar(entry[key], quote=quote)))
    return "\n".join(lines) + "\n"


def full_entry(**values):
    """An entry with every schema key present, defaults filled in."""
    entry = {k: None for k in FIELDS}
    entry["legacy"] = False
    entry["paid"] = False
    entry["qr_generated"] = False
    entry.update(values)
    if entry["legacy"]:
        for field in NON_LEGACY_FIELDS:
            if field not in values:
                del entry[field]
    return entry


# --------------------------------------------------------------------------
# Redirect front matter
# --------------------------------------------------------------------------

GENERATED_HEADER = "# GENERATED by scripts/build_go.py from _data/campaign_codes.yml. Do not edit."

# Fields a legacy entry may copy through to its redirect file.
LEGACY_FRONT_MATTER = ["note", "description", "to", "utm_source", "utm_medium",
                       "utm_campaign", "utm_content", "utm_term"]


def front_matter_fields(entry):
    """Ordered (key, value) pairs for the _go/<CODE>.md front matter."""
    code = entry["code"]
    pairs = [("permalink", "/go/%s/" % code)]
    if entry.get("legacy"):
        for key in LEGACY_FRONT_MATTER:
            if entry.get(key) is not None:
                pairs.append((key, entry[key]))
        return pairs
    description = entry.get("description")
    if _blank(description):
        parts = [entry.get(k) for k in ("series", "episode", "platform", "placement")]
        description = " / ".join(p for p in parts if p)
    if not _blank(entry.get("note")):
        pairs.append(("note", entry["note"]))
    if description:
        pairs.append(("description", description))
    pairs.append(("to", destination_with_video(entry["to"], entry.get("video_uid"))))
    for key in UTM_FIELDS:
        if not _blank(entry.get(key)):
            pairs.append((key, entry[key]))
    pairs.append(("utm_id", code))
    return pairs


def render_go_file(entry):
    lines = ["---", GENERATED_HEADER]
    for key, value in front_matter_fields(entry):
        lines.append("%s: %s" % (key, yaml_scalar(value, quote=key in ("note", "description"))))
    lines.append("---")
    return "\n".join(lines) + "\n"


DATA_HEADER = """\
# Campaign codes: the source of truth for every truemath.ai/go/<CODE> link.
#
# Edit THIS file (or use scripts/new_code.py), then run scripts/build_go.py to
# regenerate _go/*.md. Never hand-edit _go/: those files are generated.
# See "Campaign redirect links" in README.md for the full workflow.
#
# Schema, one list item per code:
#   code              six-char Crockford Base32, uppercase (required, unique)
#   campaign          campaign slug (required), e.g. exactly, later live-numbers
#   series            series slug (required)
#   episode           episode slug, or null for series-level links
#   platform          youtube, linkedin, facebook, tiktok, instagram, qr, email,
#                     podcast, trade-media
#   placement         description, pinned-comment, end-screen, bio-link, post,
#                     story, group-post, show-notes, print, slide, ad
#   paid              true for a paid ad or boosted post (utm_medium gets "paid-")
#   to                site path ("/x", "/x#section") or full http(s) URL (required)
#   video_uid         Cloudflare Stream UID, appended as ?v=; null if none
#   post_id           the platform's own ID for the post/video/ad (YouTube video
#                     ID, TikTok video ID, LinkedIn URN, Meta ad ID); null until
#                     known; set it with scripts/set_post_id.py. Never in URLs.
#   utm_source        required; lowercase, no spaces
#   utm_medium        required; lowercase, no spaces; "paid-<medium>" when paid
#   utm_campaign      required; always <campaign>-<series>
#   utm_content       required; identifies the placement, e.g. cfe-ep1-youtube-description
#   utm_term          optional
#   note              internal label; never in URLs or GA
#   created           date the code was created (YYYY-MM-DD)
#   description       fuller internal detail, optional
#   legacy            true only for codes migrated from before this system
#                     (legacy entries have no campaign, paid or post_id)
#   expires           date to retire the code, or null
#   owner             who requested or owns the code (lowercase slug)
#   destination_type  landing-page, video, playground, domain-signup,
#                     series-page, external
#   qr_generated      false, true, or a path to the QR image under campaign_assets/
#
# This repo is public: keep personal or private details out of every field,
# note and description included.
"""
