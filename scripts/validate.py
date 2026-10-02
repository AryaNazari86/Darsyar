"""Validate hamyar.me course pages against Darsyar's scraper, without touching the DB.

Mirrors bot/hamyar.py exactly, so a PASS here means the real scraper will parse it.
Two phases per the AGENT_HAMYAR_IMPORT.md protocol:
  A. does the course page expose a unit list (<ol> of links)?
  B. does every unit page yield at least one parsable Q/A pair?

Writes results incrementally so a long run can be resumed or inspected mid-flight.
"""
import json, os, re, sys, time, threading
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

OUT = "validation.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
LOCK = threading.Lock()
SESSION = requests.Session()
SESSION.headers.update(UA)


def get(url, tries=3):
    for i in range(tries):
        try:
            r = SESSION.get(url, timeout=30)
            if r.status_code == 200:
                return r.text
            if r.status_code in (404, 410):
                return None
        except Exception:
            pass
        time.sleep(1.5 * (i + 1))
    return None


# ---- parsing, copied from bot/hamyar.py so verdicts match production ----

def course_units(html):
    soup = BeautifulSoup(html, "html.parser")
    ol = soup.select_one("#block-post > div.post > div.post-content > ol")
    if not ol:
        return None
    return [a["href"] for a in ol.find_all("a") if a.get("href")]


def parse_unit(html, idx):
    soup1 = BeautifulSoup(html, "html.parser")
    content = soup1.select_one("#block-post > div.post > div.post-content")
    if content is None:
        return f"درس {idx}", []

    try:
        name = soup1.select_one(
            "#block-post > div.post > div.post-content > p:nth-child(4)"
        ).text.split(":")[-1].strip()
    except Exception:
        name = f"درس {idx}"
    if len(name) > 50:
        name = f"درس {idx}"

    qs = []
    for p in content.find_all("p"):
        t = p.text
        if t.find("پاسخ:") == -1 and t.find("جواب:") == -1:
            continue
        marker = "پاسخ:" if t.find("پاسخ:") != -1 else "جواب:"
        parts = t.split(marker)

        temp = parts[0].split("ـ")
        if len(temp[0]) >= 5:
            temp = parts[0].split("-")
        q = "".join(temp[1:] if len(temp) > 1 else temp)

        qs.append({"q": q.strip(), "a": parts[-1].strip()})
    return name, qs


def page_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return ""
    t = re.sub(r"\s+", " ", m.group(1)).strip()
    return re.sub(r"\s*[-|–]\s*همیار.*$", "", t)[:120]


# ---- driver ----

def validate(cand):
    link, grade = cand["link"], cand["grade_number"]
    rec = {"grade_number": grade, "link": link, "page_title": "", "ok": False,
           "reason": "", "unit_count": 0, "bad_units": [], "total_questions": 0, "units": []}

    html = get(link)
    if html is None:
        rec["reason"] = "course page unreachable"
        return rec
    rec["page_title"] = page_title(html)

    units = course_units(html)
    if units is None:
        rec["reason"] = "no unit list (<ol>) on page - not a course index"
        return rec
    if not units:
        rec["reason"] = "unit list present but empty"
        return rec

    rec["unit_count"] = len(units)
    for i, u in enumerate(units, 1):
        uh = get(u)
        if uh is None:
            rec["bad_units"].append(i)
            rec["units"].append({"index": i, "name": f"درس {i}", "unit_link": u,
                                 "question_count": 0, "samples": [], "error": "unreachable"})
            continue
        name, qs = parse_unit(uh, i)
        if not qs:
            rec["bad_units"].append(i)
        rec["total_questions"] += len(qs)
        rec["units"].append({"index": i, "name": name, "unit_link": u,
                             "question_count": len(qs), "samples": qs[:2]})
        time.sleep(0.25)

    rec["ok"] = not rec["bad_units"] and rec["total_questions"] > 0
    if not rec["ok"] and not rec["reason"]:
        rec["reason"] = f"{len(rec['bad_units'])}/{rec['unit_count']} units yielded no Q/A"
    return rec


def main():
    cands = json.load(open(sys.argv[1], encoding="utf-8"))
    done = {}
    if os.path.exists(OUT):
        done = {r["link"]: r for r in json.load(open(OUT, encoding="utf-8"))}
        print(f"resuming: {len(done)} already validated", file=sys.stderr)

    todo = [c for c in cands if c["link"] not in done]
    print(f"to validate: {len(todo)} (of {len(cands)})", file=sys.stderr)
    results = list(done.values())

    def work(c):
        r = validate(c)
        with LOCK:
            results.append(r)
            json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            flag = "PASS" if r["ok"] else "fail"
            print(f"[{len(results)}/{len(cands)}] {flag} g{r['grade_number']:<3} "
                  f"{r['total_questions']:>5}q {r['unit_count']:>3}u  {r['link']}"
                  f"{'' if r['ok'] else '  <- ' + r['reason'][:52]}", flush=True)
        return r

    with ThreadPoolExecutor(max_workers=5) as ex:
        list(ex.map(work, todo))

    p = [r for r in results if r["ok"]]
    print(f"\n=== {len(p)} PASS / {len(results)} validated ===")
    print(f"total parsable questions across passing courses: {sum(r['total_questions'] for r in p)}")


if __name__ == "__main__":
    main()
