# Hamyar Import Agent (Darsyar)

## Goal
Import Hamyar course question banks into Darsyar safely, without polluting the database.

## Scope
- Source website: `https://hamyar.me`
- API endpoint: `https://api.darsyar.net/scrape_hamyar`
- Inputs per course:
  - `class` (exact class name used in Darsyar DB naming style)
  - `grade_number` (numeric)
  - `link` (Hamyar course page that lists unit links)

## Required Workflow
1. Discovery
- For a target grade, find all relevant Hamyar course-level links (not random single-unit pages).
- Build a list with:
  - `grade_number`
  - `class`
  - `link`

2. Exclusion
- Exclude courses that already exist in Darsyar (based on current admin/database records).

3. Pre-insert Validation (Mandatory)
- Do **not** write to DB yet.
- Validate each course link unit-by-unit:
  - The page must contain a unit list (`ol` under post content).
  - Each unit page should yield at least one parsable Q/A pair (`پاسخ:` or `جواب:` pattern).
  - Capture 1-2 sample Q/A pairs per unit for confidence.
- Mark course as:
  - `PASS`: all units have at least one parsed Q/A
  - `FAIL`: one or more units have zero parsed Q/A

4. Human Approval
- Share:
  - candidate course list with URLs
  - validation pass/fail summary
- Wait for explicit user approval before sending any API request.

5. Insert
- Send only approved and validated courses.
- Request format (GET with query params):
  - `/scrape_hamyar?class=...&grade_number=...&link=...`
- Follow redirects (`301 -> 200`) when calling API.
- Send one course at a time.

6. Progress Reporting
- For each course:
  - validation result
  - request status and response body
  - success/failure
- Expect long waits; keep reporting until completion.

## Naming Rules
- Keep class naming consistent with existing Darsyar classes.
- Prefer exact style already used in DB (for example: `اجتماعی هفتم`, `پیام‌های آسمانی هشتم`, etc.).

## Safety Rules
- Never send insert requests before approval.
- Never send failed-validation courses unless user explicitly overrides.
- If DNS/network fails in sandbox, rerun outside sandbox with explicit approval.
