"""Drive the Darsyar scrape_hamyar endpoint over the approved course list.

One course per request, sequentially: the endpoint fetches every unit page
synchronously, so parallel calls would just contend for gunicorn's 3 workers.
Follows redirects (the API answers 301 before 200) and records every result.
"""
import json, os, subprocess, sys, time, urllib.parse

API = "https://api.darsyar.net/scrape_hamyar/"
CATALOG = os.path.expanduser("~/Desktop/darsyar_course_catalog.json")
RESULTS = os.path.expanduser("~/Desktop/darsyar_import_results.json")


def call(class_name, grade_number, link, timeout=900):
    qs = urllib.parse.urlencode({"class": class_name, "grade_number": grade_number, "link": link})
    url = f"{API}?{qs}"
    t0 = time.time()
    p = subprocess.run(
        ["curl", "-sSL", "-m", str(timeout), "-w", "\n__HTTP__%{http_code}", url],
        capture_output=True,
    )
    body = p.stdout.decode("utf-8", "replace")
    code = ""
    if "__HTTP__" in body:
        body, code = body.rsplit("__HTTP__", 1)
    return {
        "http_code": code.strip(),
        "body": body.strip()[:300],
        "seconds": round(time.time() - t0, 1),
        "curl_err": p.stderr.decode("utf-8", "replace").strip()[:200] or None,
    }


def main():
    rows = json.load(open(CATALOG, encoding="utf-8"))["approved_for_import"]
    rows.sort(key=lambda r: (r["grade_number"], -r["primary_questions"]))

    done = {}
    if os.path.exists(RESULTS):
        done = {r["class_name"]: r for r in json.load(open(RESULTS, encoding="utf-8"))}
        print(f"resuming, {len(done)} already imported", flush=True)

    out = list(done.values())
    ok = sum(1 for r in out if r.get("http_code") == "200")
    total_q = 0

    for i, row in enumerate(rows, 1):
        name = row["class_name"]
        if name in done:
            continue
        res = call(name, row["grade_number"], row["primary_link"])
        rec = {"class_name": name, "grade_number": row["grade_number"],
               "link": row["primary_link"], "expected_questions": row["primary_questions"], **res}
        out.append(rec)
        json.dump(out, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

        got = ""
        if res["http_code"] == "200" and "scraped" in res["body"]:
            got = res["body"].split()[0]
            ok += 1
            try:
                total_q += int(got)
            except ValueError:
                pass
        status = "OK " if res["http_code"] == "200" else "ERR"
        print(f"[{i}/{len(rows)}] {status} g{row['grade_number']:<3} {name[:34]:36} "
              f"expected={row['primary_questions']:<5} got={got or res['body'][:60]:<8} "
              f"{res['seconds']}s", flush=True)
        time.sleep(1.5)

    print(f"\n=== {ok}/{len(rows)} imported, {total_q} questions reported ===")
    print(f"results: {RESULTS}")


if __name__ == "__main__":
    main()
