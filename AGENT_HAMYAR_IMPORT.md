# Hamyar / Hamgamdars Course Import (Darsyar)

Runbook for refilling the Darsyar question bank from `hamyar.me` and
`hamgamdars.com`. Last executed **2026-10-02**: 48 courses, 645 units,
16,208 questions across grades 7-12.

Everything below is reproducible from this file plus `scripts/`.

---

## 0. Prerequisites

Check these before anything else; each one silently breaks the import.

| requirement | why | check |
|---|---|---|
| `Source` rows with **id 1 and 2** | the views do `Source.objects.get(id=1)` / `id=2` by hard-coded PK | `select id,name from content_source;` |
| `Grade` rows, including **id 1** | `User.grade` is `ForeignKey(default=1)`; a missing Grade 1 makes every new bot user fail with an FK violation that the blanket `except` in `bot/views.py` swallows | `select count(*) from content_grade;` |
| scraper fix present | see "Scraper quirks" below | `grep get_or_create bot/views.py` |
| app reachable over HTTPS | the endpoint answers `301` then `200`; **always use `curl -L`** | `curl -sL -o/dev/null -w '%{http_code}' https://api.darsyar.net/` |

Source id 1 = `همگام درس` (hamgamdars.com), id 2 = `همیار` (hamyar.me).

---

## 1. Pipeline

Four scripts in `scripts/`, run in order. They need `beautifulsoup4` and
`requests`; use a venv, since macOS system Python has neither (and no CA
bundle, which is why the scripts shell out to `curl` rather than urllib).

```bash
python3 -m venv /tmp/darsyar-venv
/tmp/darsyar-venv/bin/pip install beautifulsoup4 requests
```

### 1a. `discover.py` — enumerate candidate course pages

Walks `hamyar.me/sitemap.xml` recursively and keeps URLs matching
`/(soal|soalmatn|gambegam|soalat)-<grade>-<subject>/` for grades 7-12.
Writes `candidates.json`.

```bash
/tmp/darsyar-venv/bin/python scripts/discover.py
```

`robots.txt` disallows only `/wp-admin/`, so this is permitted. Hamyar also
has grade index pages at `hamyar.me/topics/paye<N>/`, useful for grades
10-12 but unreliable for 7-9, where the sitemap is better.

### 1b. `validate.py` — the mandatory gate

**Never insert without this.** Mirrors `bot/hamyar.py`'s parsing exactly, so
a PASS here means the real scraper will parse it. Two phases per course:

- does the page expose a unit list (`#block-post > div.post > div.post-content > ol`)?
- does **every** unit page yield at least one `پاسخ:` / `جواب:` pair?

```bash
/tmp/darsyar-venv/bin/python validate.py candidates_all.json
```

Writes `validation.json` incrementally (resumable; re-running skips links
already recorded). 5 workers, 0.25s between unit fetches.

Expect roughly **1 PASS in 6**. In the last run, 64 of 372 candidates passed;
230 failures were "no unit list", i.e. exam papers or single-lesson posts
rather than course indexes.

**Page type matters far more than subject:**
- `soalmatn-*` (سوالات متن) — almost always parses, high yield
- `gambegam-*` (گام به گام) — usually parses but yields far less
- `soal-*-nobat1/2` (exam papers) — never parses, no unit list
- maths and قرآن — reliably fail; the Q/A is in images

### 1c. `normalize.py` — names and de-duplication

Maps each passing page to a canonical `<subject> <grade word>` name
(+ branch suffix for grades 10-12), then merges pages that resolve to the
same subject, keeping the highest-yield one as `primary_link` and the rest in
`extra_links`. Writes `approved_for_import` into the catalog JSON.

```bash
/tmp/darsyar-venv/bin/python scripts/normalize.py
```

Last run: 64 passing pages collapsed to **48 subjects**, 16,208 primary
questions, with 1,989 more available in `extra_links`.

⚠️ **Review the output by hand.** The subject matcher is regex over page
title + slug and it does get things wrong — `ensan` matching `ensani`
mislabelled تاریخ یازدهم انسانی as انسان و محیط زیست until fixed. Also check
whether branch variants should merge (e.g. `جغرافیا یازدهم` vs
`جغرافیا یازدهم انسانی` — same book or not?).

### 1d. Human approval — REQUIRED

Present the candidate list with per-course question counts and PASS/FAIL,
and **wait for an explicit yes**. Never send inserts for failed-validation
courses unless the user overrides.

### 1e. `import_courses.py` — insert

One course per request, sequentially (the endpoint fetches every unit page
inside the request, so parallel calls just contend for gunicorn's 3 workers).

```bash
/tmp/darsyar-venv/bin/python scripts/import_courses.py
```

Reads `approved_for_import`, calls
`GET /scrape_hamyar/?class=…&grade_number=…&link=…`, appends each result to
`~/Desktop/darsyar_import_results.json`, and skips anything already recorded
there. Per-course time ran 2-56s.

**Smoke-test one small course first**, then confirm it landed before
launching the rest. If you smoke-test outside the runner, pre-seed that
course into the results file or it will be imported twice.

---

## 2. Verification

```sql
-- totals
select (select count(*) from content_class) classes,
       (select count(*) from content_unit) units,
       (select count(*) from content_question) questions,
       (select count(*) from content_class_grades) grade_links;

-- duplicates (must be empty)
select name, count(*) from content_class group by name having count(*) > 1;

-- every class must be reachable from a grade, or the bot will not show it
select c.name from content_class c
 where not exists (select 1 from content_class_grades g where g.class_id = c.id);
```

`grade_links` should equal `classes`. A class with no grade link is invisible
in the bot no matter how many questions it holds.

---

## 3. Scraper quirks that cost time

- **`cls.grades.add(...)` is the whole ballgame.** The bot builds its subject
  menu from `user.grade.classes` (`bot/methods/settings.py`, `choose_class`).
  That line was commented out for a long time, so imports "succeeded" and
  nothing appeared in the bot.
- **`.exists` vs `.exists()`** — the original guard was
  `if not Class.objects.filter(...).exists:`. A bound method is always truthy,
  so the create branch ran every time and duplicated the Class. Now
  `get_or_create`.
- **No duplicate guard.** Re-importing an existing class *adds* another full
  set of units. Check before re-running, or delete the class in admin first.
- **Unit names mostly fall back.** The name comes from
  `p:nth-child(4)`; it fails on most pages, so ~555 of 645 units end up named
  `درس N`. Cosmetic but visible to students.
- **The dash split can eat question text.** `bot/hamyar.py` strips leading
  numbering by splitting on `ـ` then `-`. A question with no numbering but a
  hyphen in the body loses everything before the hyphen.
- **Thin units.** 100 units have fewer than 5 questions; `bot/methods/test.py`
  now caps the exam sample with `min(5, len(questions))` instead of throwing.
- **hamgamdars beats hamyar for اجتماعی** — the old bank had 1,013 questions
  for `اجتماعی هفتم` from Source 1 vs 597 from hamyar. Worth a Source 1 pass
  for social studies. `scripts/discover.py` only covers hamyar; hamgamdars
  needs its own discovery (different selectors, see `bot/scraper.py`).

---

## 4. Naming rules

Keep class names consistent with what is already in the DB.

- Format: `<subject> <grade word>`, e.g. `علوم هفتم`, `مطالعات اجتماعی نهم`
- Grade words: هفتم، هشتم، نهم، دهم، یازدهم، دوازدهم
- Grades 10-12 branches (`انسانی` / `ریاضی` / `تجربی`):
  - content common to all branches → no branch suffix
  - content differing by branch → include the branch
  - shared by two branches → name both
  - examples: `ریاضی دهم تجربی`, `تاریخ یازدهم ریاضی و تجربی`,
    `فلسفه یازدهم انسانی`

---

## 5. Files

| path | what |
|---|---|
| `scripts/*.py` | the pipeline (in this repo) |
| `~/Desktop/darsyar_course_catalog.json` | full catalog: passing courses with every unit + samples, failures with reasons, `approved_for_import` |
| `~/Desktop/darsyar_import_results.json` | per-course import results, doubles as the resume ledger |
| `~/Desktop/hamyar_validation_results.json` | the original Feb 2026 validation run |

`scripts/recover.py` is a one-off that reconstructed the pre-2026-10 catalog
out of Codex session transcripts in `~/.codex`. Kept for reference; not part
of the normal flow.

---

## 6. Safety rules

- Validate before inserting, always.
- Get explicit approval before the first insert request.
- One course per request; report each result as it lands.
- Expect long waits and keep reporting until done.
- Do not leave generated candidate/result files in the repo — the catalog and
  results belong on the Desktop, the scripts belong in `scripts/`.
