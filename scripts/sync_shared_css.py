"""sync_shared_css.py: keep fellowship4free's vendored open-data-shared.css in step with the
original on jonathanlindavis.com, and keep every local asset URL in index.html content-stamped.

F4F re-plan STR-22. fellowship4free serves its own copy of the Open Data family stylesheet. This
script is the sync path that copy never had: it compares the copy with the original and, on a
difference, prints what differs and the stamp it would write. With --apply it copies the original
over the vendored file and restamps index.html. A style change still goes to a fellowship4free
preview branch and merges only on the owner's approval, like any page change; this script never
commits, pushes or switches branches.

Content stamp (the house rule, as stamp_shared_css.py and style_invariants.py compute it): sha1 of
the file's bytes with CRLF normalized to LF, first 10 hex characters, written as ?v=<stamp>. The
stylesheet link also carries an integrity attribute (sha384 of the same LF-normalized bytes, which
are the bytes the Pages build serves from git). img elements do not support integrity, so assets
get the stamp only.

Usage (run from anywhere):
  python scripts/sync_shared_css.py                  compare only; prints nothing when in step
  python scripts/sync_shared_css.py --source PATH    compare against another copy of the original
  python scripts/sync_shared_css.py --stamp          restamp index.html from the files as they are
  python scripts/sync_shared_css.py --apply          copy the original in, then restamp

Exit codes: 0 in step (or work done), 1 the copies differ (compare mode), 2 a file is missing.
Default --source is the sibling checkout ../Jonathanlindavis.com/open-data-shared.css.
"""
import argparse, base64, difflib, hashlib, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDORED = os.path.join(REPO, "open-data-shared.css")
INDEX = os.path.join(REPO, "index.html")
DEFAULT_SOURCE = os.path.join(os.path.dirname(REPO), "Jonathanlindavis.com", "open-data-shared.css")
# Local asset URLs index.html may reference: stylesheets and images under the repo root or assets/.
ASSET_RE = re.compile(r'((?:href|src)=")((?:assets/)?[A-Za-z0-9_.-]+\.(?:css|svg|png|jpg|jpeg|webp|ico))(?:\?v=[0-9a-f]+)?(")')
CSS_LINK_RE = re.compile(r'<link rel="stylesheet" href="open-data-shared\.css\?v=[0-9a-f]+"(?: integrity="[^"]*")?>')


def norm(path):
    with open(path, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")


def stamp(path):
    return hashlib.sha1(norm(path)).hexdigest()[:10]


def sri(path):
    return "sha384-" + base64.b64encode(hashlib.sha384(norm(path)).digest()).decode("ascii")


def compare(source):
    """Print nothing and return True when in step; print the difference and the stamp otherwise."""
    for p in (source, VENDORED):
        if not os.path.exists(p):
            print(f"MISSING: {p}")
            sys.exit(2)
    a, b = norm(VENDORED), norm(source)
    if a == b:
        return True
    diff = list(difflib.unified_diff(a.decode("utf-8", "replace").splitlines(), b.decode("utf-8", "replace").splitlines(),
                                     "vendored/open-data-shared.css", "original/open-data-shared.css", lineterm="", n=1))
    print(f"DIFFERENT: vendored copy ({len(a)} bytes) and original ({len(b)} bytes) differ.")
    for line in diff[:60]:
        print(line)
    if len(diff) > 60:
        print(f"... {len(diff) - 60} more diff lines")
    print(f"Stamp it would write: open-data-shared.css?v={stamp(source)} (now ?v={stamp(VENDORED)})")
    print(f"Integrity it would write: {sri(source)}")
    return False


def restamp():
    with open(INDEX, "r", encoding="utf-8", newline="") as f:
        html = f.read()
    missing = []

    def sub(m):
        rel = m.group(2)
        path = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(path):
            missing.append(rel)
            return m.group(0)
        return f"{m.group(1)}{rel}?v={stamp(path)}{m.group(3)}"

    new = ASSET_RE.sub(sub, html)
    new, n = CSS_LINK_RE.subn(f'<link rel="stylesheet" href="open-data-shared.css?v={stamp(VENDORED)}" integrity="{sri(VENDORED)}">', new)
    if missing:
        print("MISSING asset files: " + ", ".join(missing))
        sys.exit(2)
    if n != 1:
        print(f"Expected exactly one open-data-shared.css link in index.html, found {n}.")
        sys.exit(2)
    if new != html:
        with open(INDEX, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print("index.html restamped.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--stamp", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.apply:
        if not compare(a.source):
            with open(a.source, "rb") as s, open(VENDORED, "wb") as d:
                d.write(s.read())
            print("Vendored copy replaced from the original.")
        restamp()
        return 0
    if a.stamp:
        restamp()
        return 0
    return 0 if compare(a.source) else 1


if __name__ == "__main__":
    sys.exit(main())
