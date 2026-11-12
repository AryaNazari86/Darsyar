"""LLM calls, served by Cloudflare Workers AI.

This replaces the old Flask service on PythonAnywhere, which proxied to Gemini
and is now unreachable from the production server (HTTP 451, sanctions).
Workers AI is reachable from Iran and has a free daily allocation.

The old service translated Persian to English, prompted Gemini in English and
translated back. That round-trip depended on Google Translate, which is also
blocked from the server, so prompts here are Persian throughout. Pick a model
that is actually good at Persian -- see CLOUDFLARE_MODEL below.

Public contract is unchanged, so callers need no edits:
    ai(question, real_answer, user_answer) -> {"grade": <0-5 float>, "feedback": str}
    hint(question, answer)                 -> str
    tutor(question)                        -> str
"""
import json
import os
import re

import requests

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
# Measured neurons per grading call on a real question (2026-11), against the
# 10,000/day free allocation. Cost here is driven by how much a model thinks
# aloud, not by its per-token price -- see _prepare().
#   @cf/qwen/qwen3-30b-a3b-fp8                3.9  ~2570/day  (current)
#   @cf/meta/llama-3.1-8b-instruct-fp8-fast   2.2  ~4600/day  cheapest; 8B judgement
#   @cf/google/gemma-4-26b-a4b-it            16.2   ~618/day  warmest tone, 4x cost
#   @cf/zai-org/glm-4.7-flash                55.7   ~180/day  rambles, truncates
# Avoid @cf/meta/llama-3.2-3b-instruct: ignores the JSON instruction.
MODEL = os.environ.get("CLOUDFLARE_MODEL", "@cf/qwen/qwen3-30b-a3b-fp8")

TIMEOUT = 90
GRADE_MAX = 5          # strings.ai_answer renders "نمره پاسخ شما: {} از ۵"

# Every model worth using here is a reasoning model: it emits a thinking trace
# before the answer, and the trace counts against max_tokens. Budgets below are
# sized from measured traces (1,300-2,000 characters) plus the answer itself --
# too low and content comes back empty while the trace eats the whole budget.
MAX_TOKENS_GRADE = 1500
# Hints need more headroom than grading: deciding how much of the answer to
# give away takes the model longer to deliberate, and 1200 was not enough for
# gemma-4. Cheap in practice, since a hint is generated once per question and
# then cached on the row forever.
MAX_TOKENS_HINT = 2500
MAX_TOKENS_TUTOR = 2000

# Persian-Indic and Arabic-Indic digits -> ASCII, so the model compares numbers
# reliably. (The old service had a typo here that mapped ۹ to 8.)
_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


class AIUnavailable(RuntimeError):
    """Raised when Workers AI cannot be reached or returns an error.

    Callers must treat this as "no grade", never as a zero -- awarding 0 points
    because the API was down would be worse than saying nothing.
    """


def _normalise(text):
    return (text or "").translate(_DIGITS).strip()


def _prepare(messages):
    """Adapt the message list to the quirks of the configured model.

    Two adjustments, both measured rather than guessed:

    - Qwen3 thinks aloud by default, and the trace is ~75% of the token cost
      (12.8 neurons per grading vs 3.9 with it off) for no gain on a task this
      constrained. "/no_think" switches it off.
    - Gemma and Granite have no system role in their chat template, so the
      system text has to be folded into the first user turn.
    """
    model = MODEL.lower()
    messages = list(messages)

    if "qwen3" in model:
        messages = [
            {**m, "content": m["content"] + " /no_think"} if m["role"] == "system" else m
            for m in messages
        ]

    if "gemma" in model or "granite" in model:
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        rest = [m for m in messages if m["role"] != "system"]
        if system and rest:
            rest[0] = {"role": rest[0]["role"],
                       "content": f"{system}\n\n---\n\n{rest[0]['content']}"}
        messages = rest

    return messages


def _run(messages, max_tokens=512, temperature=0.3):
    """One Workers AI chat completion. Returns the assistant text."""
    if not ACCOUNT_ID or not API_TOKEN:
        raise AIUnavailable("CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN not set")

    messages = _prepare(messages)
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json={
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise AIUnavailable(f"request failed: {exc}") from exc

    try:
        payload = resp.json()
    except ValueError:
        raise AIUnavailable(f"HTTP {resp.status_code}, non-JSON body") from None

    if not payload.get("success"):
        # Daily free allocation exhausted shows up here as an error entry.
        errors = payload.get("errors") or [{"message": f"HTTP {resp.status_code}"}]
        raise AIUnavailable("; ".join(str(e.get("message", e)) for e in errors))

    result = payload.get("result") or {}

    # Three shapes in the wild: classic Workers AI returns {"response": "..."},
    # some models (gemma-4, GLM) answer OpenAI-style under choices[], and when
    # the reply is valid JSON Cloudflare helpfully pre-parses it, so "response"
    # arrives as a dict. Re-serialise that so callers always get text.
    text = result.get("response")
    if isinstance(text, (dict, list)):
        return json.dumps(text, ensure_ascii=False)

    if not text:
        choices = result.get("choices") or []
        message = (choices[0].get("message") or {}) if choices else {}
        text = message.get("content") or ""
        if not text and message.get("reasoning_content"):
            # Reasoning models spend max_tokens on the trace first; if the
            # budget runs out there, content comes back empty.
            raise AIUnavailable(
                "model returned only a reasoning trace - raise max_tokens "
                "or use a non-reasoning model"
            )

    if not text:
        raise AIUnavailable("empty response from model")
    return text.strip()


def _extract_json(text):
    """Pull the first JSON object out of a model reply.

    Small models wrap JSON in prose or ```json fences even when told not to,
    so locate the outermost braces rather than trusting the whole string.
    """
    try:
        return json.loads(text)
    except ValueError:
        pass
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise AIUnavailable(f"no JSON in reply: {text[:160]}")
    try:
        return json.loads(match.group(0))
    except ValueError:
        raise AIUnavailable(f"malformed JSON in reply: {text[:160]}") from None


GRADER_SYSTEM = f"""تو یک معلم مهربان ایرانی هستی که پاسخ دانش‌آموز را تصحیح می‌کنی.

به تو یک سوال، پاسخ درست، و پاسخ دانش‌آموز داده می‌شود.
به پاسخ دانش‌آموز نمره‌ای از ۰ تا {GRADE_MAX} بده و بازخورد کوتاهی بنویس.

قواعد نمره‌دهی:
- سخت‌گیر نباش. اگر دانش‌آموز نکات اصلیِ پاسخ درست را گفته، نمره کامل بده.
- چیزی خارج از پاسخ درست از او نخواه و پیشنهاد اضافه نده.
- اگر بیشتر از پاسخ درست توضیح داده، اشکالی ندارد و از نمره کم نکن.
- اگر پاسخ کاملا بی‌ربط یا خالی است، نمره ۰ بده.
- نمره اعشاری مجاز است (مثلا ۲.۵).

بازخورد را دوم‌شخص، فارسی، و حداکثر دو جمله بنویس.

فقط و فقط یک شیء JSON برگردان، بدون هیچ متن اضافه:
{{"grade": <عدد>, "feedback": "<بازخورد فارسی>"}}"""

# A few anchors for the scale. Kept short on purpose: every example is sent on
# every request and counts against the daily neuron allocation.
GRADER_SHOTS = [
    {
        "role": "user",
        "content": "سوال: تاریخ چه علمی است؟\n"
                   "پاسخ درست: علمی است که جنبه‌های مختلف زندگی انسان و جوامع گذشته را بررسی می‌کند و علل و نتایج اندیشه‌ها و کارهای آنان را تحلیل می‌کند.\n"
                   "پاسخ دانش‌آموز: علم چیزهای قدیمی است",
    },
    {
        "role": "assistant",
        "content": '{"grade": 0.5, "feedback": "پاسخت خیلی کلی است. باید دقیق‌تر بگویی تاریخ چه چیزهایی را بررسی و تحلیل می‌کند."}',
    },
    {
        "role": "user",
        "content": "سوال: دانشمندان علوم را چگونه تقسیم کرده‌اند؟\n"
                   "پاسخ درست: فیزیک، شیمی، زمین‌شناسی، زیست‌شناسی\n"
                   "پاسخ دانش‌آموز: به فیزیک و شیمی و زمین‌شناسی و زیست‌شناسی تقسیم کرده‌اند",
    },
    {
        "role": "assistant",
        "content": '{"grade": 5, "feedback": "کاملا درست است. آفرین!"}',
    },
]


def ai(question, real_answer, user_answer):
    """Grade a student's free-text answer. Raises AIUnavailable on failure."""
    messages = [{"role": "system", "content": GRADER_SYSTEM}]
    messages += GRADER_SHOTS
    messages.append({
        "role": "user",
        "content": (
            f"سوال: {_normalise(question)}\n"
            f"پاسخ درست: {_normalise(real_answer)}\n"
            f"پاسخ دانش‌آموز: {_normalise(user_answer)}"
        ),
    })

    data = _extract_json(_run(messages, max_tokens=MAX_TOKENS_GRADE, temperature=0.2))

    try:
        grade = float(str(data.get("grade", "")).translate(_DIGITS))
    except (TypeError, ValueError):
        raise AIUnavailable(f"non-numeric grade: {data.get('grade')!r}") from None

    feedback = str(data.get("feedback") or "").strip()
    if not feedback:
        raise AIUnavailable("model returned no feedback")

    return {"grade": max(0.0, min(float(GRADE_MAX), grade)), "feedback": feedback}


HINT_SYSTEM = """تو یک معلم ایرانی هستی. به دانش‌آموز راهنمایی می‌دهی تا خودش به پاسخ سوال برسد.

- پاسخ را مستقیم و کامل نگو.
- مبهم هم نباش؛ مسیر رسیدن به پاسخ را نشان بده.
- گفتن بخش کوچکی از پاسخ اشکالی ندارد.
- فارسی، صمیمی، و حداکثر سه جمله بنویس.
- فقط متن راهنمایی را بنویس، بدون مقدمه و بدون عنوان."""


def hint(question, answer):
    """A nudge toward the answer, as plain Persian text."""
    return _run(
        [
            {"role": "system", "content": HINT_SYSTEM},
            {"role": "user", "content": (
                f"سوال: {_normalise(question)}\n"
                f"پاسخ: {_normalise(answer)}\n"
                "راهنمایی:"
            )},
        ],
        max_tokens=MAX_TOKENS_HINT,
        temperature=0.5,
    )


TUTOR_SYSTEM = """تو «درسیار» هستی، یک معلم خصوصی هوشمند برای دانش‌آموزان ایرانی.

دانش‌آموز سوال درسی می‌پرسد و تو مثل یک معلم پاسخ می‌دهی:
- فارسی، روان، و قابل فهم برای سن مدرسه.
- پاسخ را مرحله‌به‌مرحله توضیح بده، نه فقط جواب نهایی.
- نام دانش‌آموز را نمی‌دانی، پس او را با نام صدا نزن.
- اگر سوال درسی نیست، مهربانانه به مسیر درس برگردان."""


def tutor(question):
    """Free-text tutoring answer, as plain Persian text."""
    return _run(
        [
            {"role": "system", "content": TUTOR_SYSTEM},
            {"role": "user", "content": _normalise(question)},
        ],
        max_tokens=MAX_TOKENS_TUTOR,
        temperature=0.6,
    )
