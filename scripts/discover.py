"""Discovery: enumerate hamyar.me course pages for grades 7-12 from the sitemap."""
import re, json, sys, urllib.request, urllib.parse, gzip, io

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}

def get(url, timeout=30):
    # curl rather than urllib: this Mac's Python has no CA bundle installed.
    import subprocess
    p = subprocess.run(
        ["curl", "-sSL", "--compressed", "-m", str(timeout), "-A", UA["User-Agent"], url],
        capture_output=True,
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip()[:200])
    raw = p.stdout
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace")


def sitemap_urls(root):
    """Walk a sitemap index recursively, returning every <loc>."""
    seen, out, queue = set(), [], [root]
    while queue:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            xml = get(sm)
        except Exception as e:
            print(f"  ! {sm}: {e}", file=sys.stderr)
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
        if "<sitemapindex" in xml:
            queue.extend(locs)
            print(f"  index {sm} -> {len(locs)} sub-sitemaps", file=sys.stderr)
        else:
            out.extend(locs)
            print(f"  {sm} -> {len(locs)} urls", file=sys.stderr)
    return out


# Course pages use latin slugs like soal-8-olum / soalmatn-9-olum / gambegam-9-quran
COURSE_RE = re.compile(r"/(soal|soalmatn|gambegam|soalat)[a-z0-9\-]*-(\d{1,2})-([a-z0-9\-]+)/?$", re.I)

def main():
    # grade range, defaulting to secondary school: discover.py [LOW] [HIGH]
    low = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    high = int(sys.argv[2]) if len(sys.argv) > 2 else 12

    print("fetching sitemaps...", file=sys.stderr)
    urls = sitemap_urls("https://hamyar.me/sitemap.xml")
    print(f"total urls: {len(urls)}", file=sys.stderr)

    by_grade = {}
    for u in urls:
        path = urllib.parse.urlparse(u).path
        m = COURSE_RE.search(path)
        if not m:
            continue
        grade = int(m.group(2))
        if not low <= grade <= high:
            continue
        by_grade.setdefault(grade, []).append(
            {"kind": m.group(1).lower(), "grade_number": grade, "slug": m.group(3), "link": u}
        )

    total = sum(len(v) for v in by_grade.values())
    print(f"\ncandidate course pages: {total}\n")
    for g in sorted(by_grade):
        print(f"--- grade {g}: {len(by_grade[g])} ---")
        for c in sorted(by_grade[g], key=lambda x: x["slug"]):
            print(f"   {c['kind']:9} {c['slug']:28} {c['link']}")
        print()

    json.dump(by_grade, open("candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote candidates.json", file=sys.stderr)


if __name__ == "__main__":
    main()
