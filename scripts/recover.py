"""Recover the Darsyar course catalog from Codex session transcripts.

Pulls three kinds of record out of every session that mentions the scrapers:
  - course imports:   grade_number=N | `class name` | `link`   (+ nearby question count)
  - old Class table rows:  id <tab> name <tab> grade <tab> question_count
  - PASS/FAIL validation verdicts
"""
import json, re, glob, os, sys
from collections import defaultdict

SESS = os.path.expanduser("~/.codex")


def all_text(path):
    """Yield every string value in a rollout file.

    Role-scoped extraction misses most of what matters here: the scraper URLs
    and their responses live in tool-call arguments and command output.
    """
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        stack = [o]
        while stack:
            n = stack.pop()
            if isinstance(n, str):
                if len(n) > 2:
                    yield n
            elif isinstance(n, dict):
                stack.extend(n.values())
            elif isinstance(n, list):
                stack.extend(n)


# `grade_number=10` | `دین و زندگی دهم انسانی` | `https://hamyar.me/gam-dini10-en/`
IMPORT_RE = re.compile(
    r"grade_number\s*=\s*(\d{1,2})`?\s*\|\s*`?([^`|\n]+?)`?(?:\s*\|\s*`?(https?://[^`\s|)\]]+))?\s*(?:\||\n|$)"
)
# result line: `872 questions scraped succesfully!`
COUNT_RE = re.compile(r"(\d+)\s+questions scraped succesfully")
# old Class table row: 3 <tab> اجتماعی هفتم <tab> 7 <tab> 1013
TABLE_RE = re.compile(r"^\s*(\d{1,3})\t([^\t]+?)\t(\d{1,2})\t(\d{1,5})\s*$", re.M)
VERDICT_RE = re.compile(r"(PASS|FAIL|Passed|Skipped \(failed validation\))\s*:?\s*(.+)")
BACKTICKED = re.compile(r"`([^`]+)`")


def main():
    files = set()
    for pat in ("sessions/**/*.jsonl", "archived_sessions/*.jsonl"):
        files.update(glob.glob(os.path.join(SESS, pat), recursive=True))

    imports = {}            # (grade, name) -> {link, counts:set}
    table_rows = {}         # class_id -> row
    verdicts = defaultdict(set)   # name -> {PASS/FAIL}
    hit_files = 0

    for f in sorted(files):
        blobs = list(all_text(f))
        joined = "\n".join(blobs)
        if "hamyar" not in joined and "hamgamdars" not in joined:
            continue
        hit_files += 1

        for m in TABLE_RE.finditer(joined):
            cid, name, grade, qn = m.groups()
            table_rows[int(cid)] = {
                "class_id": int(cid),
                "class_name": name.strip(),
                "grade_number": int(grade),
                "question_count": int(qn),
            }

        for b in blobs:
            for m in IMPORT_RE.finditer(b):
                grade, name, link = m.group(1), m.group(2).strip(), m.group(3)
                key = (int(grade), name)
                rec = imports.setdefault(
                    key, {"grade_number": int(grade), "class_name": name, "links": set(), "question_counts": set()}
                )
                if link:
                    rec["links"].add(link.rstrip("/") + "/")
                # a success count in the same blob, near this mention
                tail = b[m.end(): m.end() + 400]
                for c in COUNT_RE.finditer(tail):
                    rec["question_counts"].add(int(c.group(1)))

            for m in VERDICT_RE.finditer(b):
                kind = "PASS" if m.group(1).lower().startswith(("pass",)) else "FAIL"
                for nm in BACKTICKED.findall(m.group(2))[:8]:
                    nm = nm.strip()
                    if nm and not nm.startswith("http") and len(nm) < 60:
                        verdicts[nm].add(kind)

    out = {
        "recovered_from": f"{hit_files} codex sessions under ~/.codex",
        "old_class_table": [table_rows[k] for k in sorted(table_rows)],
        "course_imports": sorted(
            (
                {
                    "grade_number": v["grade_number"],
                    "class_name": v["class_name"],
                    "links": sorted(v["links"]),
                    "question_counts": sorted(v["question_counts"]),
                }
                for v in imports.values()
            ),
            key=lambda r: (r["grade_number"], r["class_name"]),
        ),
        "validation_verdicts": {k: sorted(v) for k, v in sorted(verdicts.items())},
    }

    json.dump(out, open("recovered_catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"sessions scanned with hamyar/hamgamdars mentions: {hit_files}")
    print(f"old Class table rows recovered: {len(out['old_class_table'])}")
    print(f"course imports recovered:       {len(out['course_imports'])}")
    print(f"validation verdicts:            {len(out['validation_verdicts'])}")
    tot = sum(r["question_count"] for r in out["old_class_table"])
    print(f"\ntotal questions in recovered Class rows: {tot}")
    print("\n--- old Class table ---")
    for r in out["old_class_table"]:
        print(f"  id={r['class_id']:<4} g{r['grade_number']:<3} {r['class_name']:38} {r['question_count']:>5} q")
    print("\n--- course imports with links ---")
    for r in out["course_imports"]:
        if r["links"]:
            cnt = ",".join(map(str, r["question_counts"])) or "-"
            print(f"  g{r['grade_number']:<3} {r['class_name']:36} {cnt:>8}q  {r['links'][0]}")


if __name__ == "__main__":
    main()
