"""Normalise class names and merge duplicate subjects into one import row each.

Naming follows AGENT_HAMYAR_IMPORT.md: "<subject> <grade word>", with a branch
suffix for grades 10-12 when the content is branch-specific.
"""
import json, os, re
from collections import defaultdict

GRADE_WORD = {7: "هفتم", 8: "هشتم", 9: "نهم", 10: "دهم", 11: "یازدهم", 12: "دوازدهم"}

# canonical subject <- first matching pattern against (title + slug)
SUBJECTS = [
    ("مطالعات اجتماعی", r"مطالعات|motaleat|\bmot\b|اجتماعی"),
    ("پیام‌های آسمانی", r"پیام|payam"),
    ("از من تا خدا",    r"از من تا خدا"),
    ("دین و زندگی",     r"دین و زندگی|دینی|\bdini\b"),
    ("هدیه‌های آسمانی", r"هدیه|hedie"),
    ("قرآن",            r"قرآن|quran|quarn"),
    ("آمادگی دفاعی",    r"دفاعی|defaee"),
    ("تفکر و سواد رسانه‌ای", r"تفکر و سواد|سواد رسانه|tafakor"),
    ("کار و فناوری",    r"کار و فناوری|karofan|karfan|ketabkar"),
    ("علوم و فنون ادبی", r"علوم و فنون|fonoon|olumvafonon"),
    # ensan(?!i): "ensani" means the humanities branch, not this subject
    ("انسان و محیط زیست", r"انسان و محیط|ensan(?!i)"),
    ("سلامت و بهداشت",  r"سلامت|salamat"),
    ("تحلیل فرهنگی",    r"تحلیل فرهنگی|tahlil"),
    ("جامعه شناسی",     r"جامعه\s*شناسی|jame"),
    ("روانشناسی",       r"روان\s*شناسی|ravanshenasi"),
    ("زمین شناسی",      r"زمین\s*شناسی|zamin"),
    ("جغرافیا",         r"جغرافیا|joghrafi"),
    ("تاریخ",           r"تاریخ|tarikh"),
    ("فلسفه",           r"فلسفه|falsafe"),
    ("منطق",            r"منطق|mantegh"),
    ("اقتصاد",          r"اقتصاد|eghtesad"),
    ("نگارش",           r"نگارش|negaresh"),
    ("فارسی",           r"فارسی|farsi"),
    ("عربی",            r"عربی|arabi"),
    ("زبان انگلیسی",    r"زبان|zaban"),
    ("زیست شناسی",      r"زیست|zist"),
    ("شیمی",            r"شیمی|shimi"),
    ("فیزیک",           r"فیزیک|fizik"),
    ("هندسه",           r"هندسه|hendese"),
    ("حسابان",          r"حسابان|hesaban"),
    ("ریاضی",           r"ریاضی|riazi"),
    ("علوم",            r"علوم|olum"),
]

def subject_of(title, slug):
    hay = f"{title} {slug}".lower()
    for canon, pat in SUBJECTS:
        if re.search(pat, hay, re.I):
            return canon
    return None

def branch_of(title, slug, grade):
    """Branch suffix, only meaningful for grades 10-12."""
    if grade < 10:
        return ""
    hay = f"{title} {slug}".lower()
    human = bool(re.search(r"انسانی|\be\b|-en\b|ensani", hay))
    rt = bool(re.search(r"ریاضی و تجربی|\brt\b|riazi", hay)) and "ریاضی و تجربی" in title or bool(re.search(r"ریاضی و تجربی|\brt\b", hay))
    if human and rt:
        return ""              # shared across branches -> no suffix
    if human:
        return "انسانی"
    if rt:
        return "ریاضی و تجربی"
    return ""

def main():
    val = json.load(open(os.path.expanduser("~/Desktop/darsyar_course_catalog.json"), encoding="utf-8"))
    passed = val["passed_courses"]

    groups = defaultdict(list)
    unmatched = []
    for r in passed:
        slug = r["link"].rstrip("/").rsplit("/", 1)[-1]
        subj = subject_of(r["page_title"], slug)
        if not subj:
            unmatched.append(r)
            continue
        g = r["grade_number"]
        name = " ".join(x for x in (subj, GRADE_WORD[g], branch_of(r["page_title"], slug, g)) if x)
        groups[(g, name)].append(r)

    rows = []
    for (g, name), members in sorted(groups.items(), key=lambda kv: (kv[0][0], -max(m["total_questions"] for m in kv[1]))):
        members.sort(key=lambda m: -m["total_questions"])
        primary = members[0]
        rows.append({
            "grade_number": g,
            "class_name": name,
            "primary_link": primary["link"],
            "primary_questions": primary["total_questions"],
            "primary_units": primary["unit_count"],
            "merged_from": [
                {"link": m["link"], "questions": m["total_questions"], "units": m["unit_count"],
                 "page_title": m["page_title"]} for m in members
            ],
            "extra_links": [m["link"] for m in members[1:]],
            "extra_questions": sum(m["total_questions"] for m in members[1:]),
        })

    val["approved_for_import"] = rows
    val["unmatched_subject"] = [{"grade_number": r["grade_number"], "link": r["link"],
                                 "page_title": r["page_title"], "total_questions": r["total_questions"]}
                                for r in unmatched]
    path = os.path.expanduser("~/Desktop/darsyar_course_catalog.json")
    json.dump(val, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"{len(passed)} passing courses -> {len(rows)} merged subjects")
    print(f"primary questions: {sum(r['primary_questions'] for r in rows)}")
    print(f"extra (second source for same subject): {sum(r['extra_questions'] for r in rows)}")
    if unmatched:
        print(f"\nunmatched subject ({len(unmatched)}): " + ", ".join(r['page_title'][:28] for r in unmatched))
    print()
    for g in sorted(GRADE_WORD):
        rs = [r for r in rows if r["grade_number"] == g]
        if not rs:
            continue
        print(f"--- GRADE {g}: {len(rs)} subjects, {sum(r['primary_questions'] for r in rs)}q ---")
        for r in rs:
            extra = f"  (+{r['extra_questions']}q from {len(r['extra_links'])} more)" if r["extra_links"] else ""
            print(f"  {r['primary_questions']:>5}q {r['primary_units']:>3}u  {r['class_name']:34} "
                  f"{r['primary_link'].replace('https://hamyar.me/','')}{extra}")
        print()

if __name__ == "__main__":
    main()
