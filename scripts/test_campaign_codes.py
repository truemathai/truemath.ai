#!/usr/bin/env python3
"""Tests for the campaign code scripts. Standard library + PyYAML only.

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import contextlib
import datetime
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_go  # noqa: E402
import campaign_codes as cc  # noqa: E402
import migrate_existing_codes  # noqa: E402
import new_code  # noqa: E402
import set_post_id  # noqa: E402

TODAY = datetime.date(2026, 11, 5)
UID = "86358cfbfbf38b02338ddc9cc2c9ece8"


def good(**over):
    entry = cc.full_entry(
        code="R7K9XM", campaign="exactly", series="cleared-for-exactness", episode="ep1-weight-and-balance",
        platform="youtube", placement="description",
        to="/series/cleared-for-exactness#weight-and-balance",
        utm_source="youtube", utm_medium="video", utm_campaign="exactly-cleared-for-exactness",
        utm_content="cfe-ep1-youtube-description", note="CfE Ep1 YouTube description link",
        created=TODAY, owner="bill", destination_type="landing-page")
    entry.update(over)
    return entry


def legacy(**over):
    entry = cc.full_entry(code="099AWD", to="/introduction.html", utm_campaign="099AWD",
                          note="Intro video player", created=datetime.date(2026, 7, 27),
                          legacy=True)
    entry.update(over)
    return entry


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run_quietly(fn, *args, **kwargs):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fn(*args, **kwargs)
    return rc, out.getvalue(), err.getvalue()


class TempRepo(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        os.makedirs(os.path.join(self.root, "_data"))
        os.makedirs(os.path.join(self.root, "_go"))
        self.data = os.path.join(self.root, "_data", "campaign_codes.yml")
        self.go = os.path.join(self.root, "_go")

    def errors(self, entry):
        return cc.validate_entry(entry, repo_root=self.root, today=TODAY)[0]

    def warnings(self, entry):
        return cc.validate_entry(entry, repo_root=self.root, today=TODAY)[1]


class TestDerivation(unittest.TestCase):
    def test_abbreviation(self):
        self.assertEqual(cc.series_abbr("cleared-for-exactness"), "cfe")
        self.assertEqual(cc.series_abbr("the-cap-table"), "tct")
        self.assertEqual(cc.series_abbr("dana"), "dana")

    def test_utm(self):
        self.assertEqual(
            cc.derive_utm("exactly", "cleared-for-exactness", "ep1-weight-and-balance",
                          "youtube", "description"),
            {"utm_source": "youtube", "utm_medium": "video",
             "utm_campaign": "exactly-cleared-for-exactness",
             "utm_content": "cfe-ep1-youtube-description"})
        self.assertEqual(
            cc.derive_utm("exactly", "cleared-for-exactness", None, "qr", "print")["utm_content"],
            "cfe-series-qr-print")
        self.assertEqual(
            cc.derive_utm("exactly", "dana", "ep2-x", "tiktok", "bio-link", abbr="dn")["utm_content"],
            "dn-ep2-tiktok-bio-link")
        self.assertEqual(cc.utm_campaign_for("live-numbers", "dana"), "live-numbers-dana")

    def test_paid(self):
        utm = cc.derive_utm("exactly", "cleared-for-exactness", "ep1-x", "linkedin", "ad", paid=True)
        self.assertEqual((utm["utm_medium"], utm["utm_content"]),
                         ("paid-social", "cfe-ep1-linkedin-ad"))
        self.assertEqual(cc.utm_medium_for("youtube", True), "paid-video")

    def test_medium_map(self):
        expected = {"youtube": "video", "tiktok": "video", "instagram": "video",
                    "linkedin": "social", "facebook": "social", "qr": "qr", "email": "email",
                    "podcast": "podcast", "trade-media": "referral"}
        for platform, medium in expected.items():
            self.assertEqual(cc.derive_utm("c", "s", None, platform, "post")["utm_medium"], medium)
        self.assertEqual(sorted(expected), sorted(cc.PLATFORMS))

    def test_codes_are_crockford_and_unique(self):
        for _ in range(200):
            self.assertRegex(cc.random_code(), cc.CODE_RE)
        existing = {"AAAAAA"}
        self.assertNotIn(cc.new_unique_code(existing), existing)

    def test_video_before_fragment(self):
        self.assertEqual(cc.destination_with_video("/a#b", UID), "/a?v=%s#b" % UID)
        self.assertEqual(cc.destination_with_video("/a?x=1#b", UID), "/a?x=1&v=%s#b" % UID)
        self.assertEqual(cc.destination_with_video("/a", None), "/a")


class TestValidation(TempRepo):
    def test_good_entry(self):
        self.assertEqual(self.errors(good()), [])
        self.assertEqual(self.errors(legacy()), [])

    def test_code_format(self):
        for bad in ("R7K9X", "R7K9XMM", "r7k9xm", "R7K9XI", "R7K9XL", "R7K9XO", "R7K9XU", None):
            self.assertTrue(self.errors(good(code=bad)), bad)

    def test_duplicate_code_is_error_and_shared_content_warns(self):
        errors, _ = cc.validate_entries([good(), good()], repo_root=self.root, today=TODAY)
        self.assertTrue(any("duplicate code" in e for e in errors))
        errors, warnings = cc.validate_entries([good(), good(code="HR67H3")],
                                               repo_root=self.root, today=TODAY)
        self.assertEqual(errors, [])
        self.assertTrue(any("share utm_content" in w for w in warnings))

    def test_to(self):
        for ok in ("/", "/x#section", "https://app.truemath.ai/signup", "http://x.io/a?b=c#d"):
            self.assertEqual(self.errors(good(to=ok)), [], ok)
        for bad in (None, "", "x/y", "//evil.com", "ftp://x", "/a b", "https://"):
            self.assertTrue(self.errors(good(to=bad)), bad)

    def test_required_utm_except_legacy(self):
        for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content"):
            self.assertTrue(self.errors(good(**{field: None})), field)
            self.assertTrue(self.errors(good(**{field: ""})), field)
        self.assertEqual(self.errors(legacy(utm_source=None, utm_medium=None)), [])

    def test_utm_lowercase_no_spaces_except_legacy(self):
        self.assertTrue(self.errors(good(utm_source="YouTube")))
        self.assertTrue(self.errors(good(utm_content="cfe ep1")))
        self.assertTrue(self.errors(good(utm_term="Big Term")))
        self.assertEqual(self.errors(legacy(utm_campaign="099AWD", utm_source="Acme Pod")), [])

    def test_campaign(self):
        self.assertTrue(self.errors(good(utm_campaign="cleared-for-exactness")))
        self.assertTrue(self.errors(good(utm_campaign="exactly-other-series")))
        self.assertTrue(self.errors(good(campaign=None)))
        self.assertTrue(self.errors(good(campaign="Exactly!")))
        self.assertEqual(self.errors(good(campaign="live-numbers",
                                          utm_campaign="live-numbers-cleared-for-exactness")), [])

    def test_legacy_has_no_new_fields(self):
        self.assertNotIn("campaign", legacy())
        self.assertNotIn("post_id", legacy())
        self.assertTrue(self.errors(legacy(campaign="exactly")))
        self.assertTrue(self.errors(legacy(paid=True)))
        self.assertTrue(self.errors(legacy(post_id="abc")))

    def test_paid_field(self):
        self.assertEqual(self.errors(good(paid=True, placement="ad", utm_medium="paid-video")), [])
        self.assertTrue(self.errors(good(paid="yes")))

    def test_post_id(self):
        self.assertEqual(self.errors(good(post_id="dQw4w9WgXcQ")), [])
        self.assertTrue(self.errors(good(post_id="dQw4w9WgXc")))      # 10 chars
        self.assertTrue(self.errors(good(post_id="dQw4w9WgXc!")))
        self.assertTrue(self.errors(good(post_id="has space")))
        self.assertTrue(self.errors(good(post_id=1234567890)))        # unquoted number
        linkedin = dict(platform="linkedin", utm_source="linkedin", utm_medium="social",
                        placement="post")
        self.assertEqual(self.errors(good(post_id="urn:li:share:7261234567890", **linkedin)), [])
        self.assertTrue(self.errors(good(post_id="urn li", **linkedin)))

    def test_required_series_platform_placement(self):
        for field in ("series", "platform", "placement"):
            self.assertTrue(self.errors(good(**{field: None})), field)
        self.assertTrue(self.errors(good(platform="myspace")))
        self.assertTrue(self.errors(good(placement="banner")))
        self.assertTrue(self.errors(good(series="Cleared For Exactness")))

    def test_pii_warning(self):
        self.assertTrue(self.warnings(good(note="ask jane@example.com")))
        self.assertTrue(self.warnings(good(description="call 503-555-0100")))
        self.assertEqual(self.warnings(good()), [])

    def test_created(self):
        self.assertTrue(self.errors(good(created=None)))
        self.assertTrue(self.errors(good(created="2026-13-01")))
        self.assertEqual(self.errors(good(created="2026-11-05")), [])

    def test_video_uid(self):
        self.assertEqual(self.errors(good(video_uid=UID)), [])
        self.assertTrue(self.errors(good(video_uid=UID.upper())))
        self.assertTrue(self.errors(good(video_uid="abc")))
        self.assertTrue(self.errors(good(video_uid=UID, to="/introduction.html?v=" + UID)))

    def test_expires(self):
        self.assertTrue(self.errors(good(expires="soon")))
        self.assertTrue(self.errors(good(expires=TODAY - datetime.timedelta(days=1))))
        self.assertEqual(self.warnings(good(expires=TODAY + datetime.timedelta(days=30))), [])
        old = good(created=datetime.date(2026, 1, 1), expires=datetime.date(2026, 2, 1))
        self.assertEqual(self.errors(old), [])
        self.assertTrue(any("expired" in w for w in self.warnings(old)))

    def test_owner_and_destination_type(self):
        self.assertEqual(self.errors(good(owner="steve-brown")), [])
        self.assertTrue(self.errors(good(owner="Steve Brown")))
        for dtype in cc.DESTINATION_TYPES:
            self.assertEqual(self.errors(good(destination_type=dtype)), [])
        self.assertTrue(self.errors(good(destination_type="homepage")))

    def test_qr_generated(self):
        self.assertEqual(self.errors(good(qr_generated=True)), [])
        self.assertEqual(self.errors(good(qr_generated=False)), [])
        self.assertTrue(self.errors(good(qr_generated="campaign_assets/qr/R7K9XM.png")))
        os.makedirs(os.path.join(self.root, "campaign_assets", "qr"))
        open(os.path.join(self.root, "campaign_assets", "qr", "R7K9XM.png"), "w").close()
        self.assertEqual(self.errors(good(qr_generated="campaign_assets/qr/R7K9XM.png")), [])
        self.assertTrue(self.errors(good(qr_generated="images/R7K9XM.png")))
        self.assertTrue(self.errors(good(qr_generated="campaign_assets/../CNAME")))
        self.assertTrue(self.errors(good(qr_generated=3)))

    def test_unknown_field(self):
        self.assertTrue(self.errors(good(utm_souce="youtube")))


class TestYamlEmitter(unittest.TestCase):
    def test_round_trip(self):
        entries = [good(), legacy(description='Quote "this" — and `that`: ok'),
                   good(code="000001", utm_term="yes", note="null")]
        text = "".join(cc.entry_to_yaml(e) for e in entries)
        self.assertEqual(cc.parse_entries(text), entries)

    def test_generated_front_matter(self):
        self.assertEqual(cc.render_go_file(good(video_uid=None)), "\n".join([
            "---", cc.GENERATED_HEADER,
            "permalink: /go/R7K9XM/",
            'note: "CfE Ep1 YouTube description link"',
            'description: "cleared-for-exactness / ep1-weight-and-balance / youtube / description"',
            "to: /series/cleared-for-exactness#weight-and-balance",
            "utm_source: youtube", "utm_medium: video",
            "utm_campaign: exactly-cleared-for-exactness",
            "utm_content: cfe-ep1-youtube-description",
            "utm_id: R7K9XM", "---", ""]))
        self.assertIn("to: /series/cleared-for-exactness?v=%s#weight-and-balance" % UID,
                      cc.render_go_file(good(video_uid=UID)))
        # post_id, paid and campaign stay out of the redirect file (never in URLs).
        text = cc.render_go_file(good(post_id="dQw4w9WgXcQ", paid=True))
        self.assertNotIn("dQw4w9WgXcQ", text)
        self.assertNotIn("paid:", text)
        self.assertNotIn("campaign: exactly\n", text)

    def test_legacy_front_matter_is_exact(self):
        text = cc.render_go_file(legacy())
        self.assertNotIn("utm_id", text)
        self.assertNotIn("utm_source", text)  # layout default applies
        self.assertIn("utm_campaign: 099AWD", text)


class TestBuildGo(TempRepo):
    def write(self, entries):
        with open(self.data, "w") as f:
            f.write(cc.DATA_HEADER + "".join("\n" + cc.entry_to_yaml(e) for e in entries))

    def build(self, *argv):
        return run_quietly(build_go.main, list(argv), data_file=self.data,
                           go_dir=self.go, repo_root=self.root)

    def test_build_then_check(self):
        self.write([good(), legacy()])
        open(os.path.join(self.go, "STALE1.md"), "w").close()
        rc, _, err = self.build("--check")
        self.assertEqual(rc, 1)
        self.assertIn("extra", err)
        self.assertEqual(self.build()[0], 0)
        self.assertEqual(sorted(os.listdir(self.go)), ["099AWD.md", "R7K9XM.md"])
        self.assertEqual(self.build("--check")[0], 0)
        with open(os.path.join(self.go, "R7K9XM.md"), "a") as f:
            f.write("# hand edit\n")
        rc, _, err = self.build("--check")
        self.assertEqual(rc, 1)
        self.assertIn("outdated", err)

    def test_invalid_writes_nothing(self):
        self.write([good(code="BAD")])
        rc, _, _ = self.build()
        self.assertEqual(rc, 1)
        self.assertEqual(os.listdir(self.go), [])

    def test_expired_warns_in_check(self):
        self.write([good(created=datetime.date(2026, 1, 1), expires=datetime.date(2026, 2, 1))])
        self.build()
        rc, out, _ = self.build("--check")
        self.assertEqual(rc, 0)
        self.assertIn("expired", out)


class TestNewCode(TempRepo):
    def setUp(self):
        super().setUp()
        with open(self.data, "w") as f:
            f.write(cc.DATA_HEADER + "\n" + cc.entry_to_yaml(legacy()))

    def run_cli(self, *argv):
        return run_quietly(new_code.main, list(argv), data_file=self.data, repo_root=self.root)

    def test_single(self):
        rc, out, err = self.run_cli(
            "--campaign", "exactly", "--series", "cleared-for-exactness", "--episode", "ep1-weight-and-balance",
            "--platform", "youtube", "--placement", "description",
            "--to", "/series/cleared-for-exactness#weight-and-balance",
            "--note", "CfE Ep1 YouTube description link")
        self.assertEqual(rc, 0, err)
        with open(self.data) as f:
            text = f.read()
        self.assertTrue(text.startswith(cc.DATA_HEADER))  # comments preserved
        entries = cc.parse_entries(text)
        self.assertEqual(len(entries), 2)
        new = entries[1]
        self.assertIn(cc.go_url(new["code"]), out)
        self.assertEqual(new["utm_content"], "cfe-ep1-youtube-description")
        self.assertEqual(new["utm_campaign"], "exactly-cleared-for-exactness")
        self.assertEqual((new["paid"], new["post_id"]), (False, None))
        self.assertEqual(new["owner"], "bill")
        self.assertEqual(new["destination_type"], "landing-page")
        self.assertEqual(new["created"], datetime.date.today())
        self.assertFalse(new["legacy"])

    def test_dry_run_writes_nothing(self):
        with open(self.data) as f:
            before = f.read()
        rc, _, _ = self.run_cli("--campaign", "exactly", "--series", "dana", "--platform", "qr", "--placement", "print",
                                "--to", "/", "--dry-run")
        self.assertEqual(rc, 0)
        with open(self.data) as f:
            self.assertEqual(f.read(), before)

    def test_invalid_single_writes_nothing(self):
        with open(self.data) as f:
            before = f.read()
        rc, _, _ = self.run_cli("--campaign", "exactly", "--series", "dana", "--platform", "qr", "--placement", "print",
                                "--to", "not-a-path")
        self.assertEqual(rc, 1)
        with open(self.data) as f:
            self.assertEqual(f.read(), before)

    def test_single_paid_with_post_id(self):
        rc, _, err = self.run_cli("--campaign", "exactly", "--series", "dana", "--episode", "ep1-x",
                                  "--platform", "youtube", "--placement", "ad", "--paid",
                                  "--post-id", "dQw4w9WgXcQ", "--to", "/")
        self.assertEqual(rc, 0, err)
        new = cc.load_entries(self.data)[-1]
        self.assertEqual((new["utm_medium"], new["utm_content"], new["post_id"], new["paid"]),
                         ("paid-video", "dana-ep1-youtube-ad", "dQw4w9WgXcQ", True))

    def test_campaign_required(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                new_code.main(["--series", "dana", "--platform", "qr", "--placement", "print",
                               "--to", "/"], data_file=self.data, repo_root=self.root)

    def batch_file(self, rows, header="campaign,series,episode,platform,placement,to,video_uid,note"):
        path = os.path.join(self.root, "launch.csv")
        with open(path, "w") as f:
            f.write(header + "\n" + "\n".join(rows) + "\n")
        return path

    def test_batch(self):
        path = self.batch_file([
            "exactly,cleared-for-exactness,ep1-weight-and-balance,youtube,description,/s#a,,One",
            "exactly,cleared-for-exactness,,qr,print,/s,%s,Two" % UID,
        ])
        rc, _, err = self.run_cli("--batch", path)
        self.assertEqual(rc, 0, err)
        entries = cc.parse_entries(read(self.data))
        self.assertEqual([e["utm_content"] for e in entries[1:]],
                         ["cfe-ep1-youtube-description", "cfe-series-qr-print"])
        with open(os.path.join(self.root, "launch.codes.csv")) as f:
            lines = f.read().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertIn(cc.go_url(entries[1]["code"]), lines[1])

    def test_batch_all_or_nothing(self):
        with open(self.data) as f:
            before = f.read()
        path = self.batch_file([
            "exactly,cleared-for-exactness,ep1,youtube,description,/s,,Good",
            "exactly,cleared-for-exactness,ep1,myspace,description,/s,,Bad platform",
        ])
        rc, _, err = self.run_cli("--batch", path)
        self.assertEqual(rc, 1)
        self.assertIn("row 3", err)
        with open(self.data) as f:
            self.assertEqual(f.read(), before)
        self.assertFalse(os.path.exists(os.path.join(self.root, "launch.codes.csv")))

    def test_batch_columns(self):
        rc, _, err = self.run_cli("--batch", self.batch_file(
            ["dana,,qr,print,/,,n"], header="series,episode,platform,placement,to,video_uid,note"))
        self.assertEqual(rc, 1)
        self.assertIn("missing column", err)
        rc, _, _ = self.run_cli("--batch", self.batch_file(
            ["exactly,dana,,qr,print,/,,n,x"],
            header="campaign,series,episode,platform,placement,to,video_uid,note,bogus"))
        self.assertEqual(rc, 1)

    def test_batch_optional_columns(self):
        header = ("campaign,series,episode,platform,placement,to,video_uid,note,description,abbr,"
                  "utm_term,owner,destination_type,expires,qr_generated,paid,post_id")
        path = self.batch_file([
            "exactly,dana,ep2-x,email,post,/,,n,d,dn,t,elizabeth,playground,2027-01-01,true,,",
            "exactly,dana,ep2-x,linkedin,ad,/,,n,,,,,,,,true,urn:li:sponsoredContent:42",
        ], header=header)
        rc, _, err = self.run_cli("--batch", path)
        self.assertEqual(rc, 0, err)
        first, second = cc.parse_entries(read(self.data))[-2:]
        self.assertEqual((first["utm_content"], first["utm_term"], first["owner"],
                          first["destination_type"], first["expires"], first["qr_generated"],
                          first["description"], first["paid"], first["post_id"]),
                         ("dn-ep2-email-post", "t", "elizabeth", "playground",
                          datetime.date(2027, 1, 1), True, "d", False, None))
        self.assertEqual((second["utm_medium"], second["utm_content"], second["post_id"]),
                         ("paid-social", "dana-ep2-linkedin-ad", "urn:li:sponsoredContent:42"))
        self.assertEqual(second["utm_campaign"], "exactly-dana")

    def test_batch_bad_paid_value(self):
        path = self.batch_file(["exactly,dana,,qr,print,/,,n,maybe"],
                               header="campaign,series,episode,platform,placement,to,video_uid,note,paid")
        rc, _, err = self.run_cli("--batch", path)
        self.assertEqual(rc, 1)
        self.assertIn("paid", err)


class TestSetPostId(TempRepo):
    def setUp(self):
        super().setUp()
        self.text = (cc.DATA_HEADER + "\n" + cc.entry_to_yaml(legacy()) + "\n"
                     + cc.entry_to_yaml(good()) + "\n# trailing comment\n")
        with open(self.data, "w") as f:
            f.write(self.text)

    def run_cli(self, *argv):
        return run_quietly(set_post_id.main, list(argv), data_file=self.data, repo_root=self.root)

    def test_sets_and_preserves_layout(self):
        rc, _, err = self.run_cli("R7K9XM", "dQw4w9WgXcQ")
        self.assertEqual(rc, 0, err)
        after = read(self.data)
        self.assertEqual(after, self.text.replace("  post_id: null\n", "  post_id: dQw4w9WgXcQ\n"))
        self.assertEqual(cc.load_entries(self.data)[1]["post_id"], "dQw4w9WgXcQ")

    def test_lowercase_code_accepted(self):
        self.assertEqual(self.run_cli("r7k9xm", "dQw4w9WgXcQ")[0], 0)

    def test_refuses_overwrite_without_force(self):
        self.run_cli("R7K9XM", "dQw4w9WgXcQ")
        rc, _, err = self.run_cli("R7K9XM", "aaaaaaaaaaa")
        self.assertEqual(rc, 1)
        self.assertIn("--force", err)
        self.assertEqual(self.run_cli("R7K9XM", "aaaaaaaaaaa", "--force")[0], 0)
        self.assertEqual(cc.load_entries(self.data)[1]["post_id"], "aaaaaaaaaaa")

    def test_invalid_or_unknown_writes_nothing(self):
        for argv in (("R7K9XM", "too-short"), ("ZZZZZZ", "dQw4w9WgXcQ"), ("099AWD", "dQw4w9WgXcQ")):
            rc, _, _ = self.run_cli(*argv)
            self.assertEqual(rc, 1, argv)
            self.assertEqual(read(self.data), self.text)

    def test_numeric_id_is_quoted(self):
        entry = good(platform="facebook", utm_source="facebook", utm_medium="social",
                     placement="post")
        with open(self.data, "w") as f:
            f.write(cc.entry_to_yaml(entry))
        self.assertEqual(self.run_cli("R7K9XM", "120210000000000")[0], 0)
        self.assertIn('post_id: "120210000000000"', read(self.data))
        self.assertEqual(cc.load_entries(self.data)[0]["post_id"], "120210000000000")

    def test_inserts_key_when_missing(self):
        entry = good()
        del entry["post_id"]
        with open(self.data, "w") as f:
            f.write(cc.entry_to_yaml(entry))
        self.assertEqual(self.run_cli("R7K9XM", "dQw4w9WgXcQ")[0], 0)
        self.assertEqual(cc.load_entries(self.data)[0]["post_id"], "dQw4w9WgXcQ")


class TestMigration(TempRepo):
    def test_migrates_exactly(self):
        original = ('---\npermalink: /go/Q3XR9T/\nnote: "Podcast — read"\n'
                    "to: https://app.truemath.ai/signup\nutm_source: acme-podcast\n"
                    "utm_medium: sponsorship\nutm_campaign: podcast-2026h1\n---\n")
        path = os.path.join(self.go, "Q3XR9T.md")
        with open(path, "w") as f:
            f.write(original)
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
        subprocess.check_call(["git", "init", "-q"], cwd=self.root)
        subprocess.check_call(git + ["add", "_go"], cwd=self.root)
        env = dict(os.environ, GIT_AUTHOR_DATE="2026-07-21T12:00:00",
                   GIT_COMMITTER_DATE="2026-07-21T12:00:00")
        subprocess.check_call(git + ["commit", "-qm", "add"], cwd=self.root, env=env)

        rc, _, err = run_quietly(migrate_existing_codes.main, go_dir=self.go,
                                 data_file=self.data, repo_root=self.root)
        self.assertEqual(rc, 0, err)
        entry = cc.load_entries(self.data)[0]
        self.assertTrue(entry["legacy"])
        self.assertEqual(entry["created"], datetime.date(2026, 7, 21))
        self.assertEqual(entry["utm_campaign"], "podcast-2026h1")
        self.assertIsNone(entry["utm_content"])

        # Regenerated file = original plus the GENERATED header line.
        run_quietly(build_go.main, [], data_file=self.data, go_dir=self.go, repo_root=self.root)
        with open(path) as f:
            regenerated = f.read()
        self.assertEqual(regenerated.replace(cc.GENERATED_HEADER + "\n", ""), original)

        # Re-running skips codes already migrated.
        rc, out, _ = run_quietly(migrate_existing_codes.main, go_dir=self.go,
                                 data_file=self.data, repo_root=self.root)
        self.assertEqual(len(cc.load_entries(self.data)), 1)


class TestRepoData(unittest.TestCase):
    """The committed data file is valid and _go/ is in sync with it."""

    def test_repo_in_sync(self):
        rc, out, err = run_quietly(build_go.main, ["--check"])
        self.assertEqual(rc, 0, err)


if __name__ == "__main__":
    unittest.main()
