"""Deadline Math: can a model convert a published deadline into the reader's local time?

Two case sets: "standard" (20 cases in 6 categories) and "hard" (11 exploratory cases, written after the standard
pilot to separate the strongest models). Every case carries a hand-written answer and one computed with `zoneinfo`;
if they disagree, importing this file fails, so a typo can never reach Kaggle.

From the KaggleBench root (Git Bash):

    set -a; . ./.env; set +a
    .venv/Scripts/python.exe benchmark/deadline_math.py            # the standard cases against the default model
    .venv/Scripts/python.exe benchmark/piloto.py                    # local pilot across several models
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import re
import time

import kaggle_benchmarks as kbench

READERS = {
    "Madrid, Spain": "Europe/Madrid",
    "Lima, Peru": "America/Lima",
    "Tokyo, Japan": "Asia/Tokyo",
    "Los Angeles, USA": "America/Los_Angeles",
    "New York, USA": "America/New_York",
    "Madrid, Spain, but that week I'm traveling in New York, USA, and I need New York time": "America/New_York",
    "London, UK": "Europe/London",
}


@dataclass(frozen=True)
class Case:
    id: str
    category: str
    statement: str  # what the page says, as the reader would see it
    reader: str  # key of READERS
    source_local: str  # deadline date and time in the source zone, "YYYY-MM-DD HH:MM"
    source_zone: str  # IANA zone (PT, ET, "Sydney time"...) or fixed offset "+HH:MM" (PDT, IST, AoE...)
    expected: str  # answer in the reader's local time, worked out by hand
    shift_minutes: int = 0  # duration added in absolute time ("72 hours later", a Unix timestamp...)
    target: str = "that deadline"  # what is asked for, when it is not the deadline itself
    naive: str = ""  # paired set only: the answer you get by applying the usual offset or adding clock hours


CASES = [
    # Base: no change of day or of clock rules.
    Case("base-1", "base", "Submissions close September 30, 2026 at 5:00 PM ET.", "Madrid, Spain",
         "2026-09-30 17:00", "America/New_York", "2026-09-30 23:00"),
    Case("base-2", "base", "Deadline: July 15, 2026, 12:00 UTC.", "Lima, Peru",
         "2026-07-15 12:00", "+00:00", "2026-07-15 07:00"),
    Case("base-3", "base", "Applications are due June 1, 2026 at 9:00 AM CEST.", "Tokyo, Japan",
         "2026-06-01 09:00", "+02:00", "2026-06-01 16:00"),
    # The deadline falls on a different day for the reader.
    Case("roll-1", "day-rollover", "The contest ends on October 11, 2026 at 11:59 PM PDT.", "Madrid, Spain",
         "2026-10-11 23:59", "-07:00", "2026-10-12 08:59"),
    Case("roll-2", "day-rollover", "Entries close March 3, 2026 at 11:59 PM PST.", "Madrid, Spain",
         "2026-03-03 23:59", "-08:00", "2026-03-04 08:59"),
    Case("roll-3", "day-rollover", "Deadline: 10:00 AM CET, February 2, 2026.", "Los Angeles, USA",
         "2026-02-02 10:00", "+01:00", "2026-02-02 01:00"),
    Case("roll-4", "day-rollover", "Submit by 8:00 AM JST on May 5, 2026.", "Lima, Peru",
         "2026-05-05 08:00", "+09:00", "2026-05-04 18:00"),
    # Autumn gap: Europe leaves summer time on Oct 25, 2026 and the US on Nov 1, 2026.
    Case("dst-oct-1", "dst-gap-autumn", "Submissions close October 28, 2026 at 11:59 PM PT.", "Madrid, Spain",
         "2026-10-28 23:59", "America/Los_Angeles", "2026-10-29 07:59"),
    Case("dst-oct-2", "dst-gap-autumn", "The live session starts October 30, 2026, 9:00 AM ET.", "Madrid, Spain",
         "2026-10-30 09:00", "America/New_York", "2026-10-30 14:00"),
    Case("dst-oct-3", "dst-gap-autumn", "Voting closes October 27, 2026 at 18:00 CET.", "New York, USA",
         "2026-10-27 18:00", "+01:00", "2026-10-27 13:00"),
    Case("dst-oct-4", "dst-gap-autumn", "Final round closes November 2, 2026 at 11:59 PM PT.", "Madrid, Spain",
         "2026-11-02 23:59", "America/Los_Angeles", "2026-11-03 08:59"),
    # Spring gap: the US starts summer time on Mar 8, 2026 and Europe on Mar 29, 2026.
    Case("dst-mar-1", "dst-gap-spring", "Entries close March 20, 2026 at 11:59 PM PT.", "Madrid, Spain",
         "2026-03-20 23:59", "America/Los_Angeles", "2026-03-21 07:59"),
    Case("dst-mar-2", "dst-gap-spring", "The webinar starts March 25, 2026, 12:00 PM CET.", "Los Angeles, USA",
         "2026-03-25 12:00", "+01:00", "2026-03-25 04:00"),
    # Wording that is easy to misread: 12 AM, AoE, 12 PM.
    Case("sem-1", "wording", "Deadline: 12:00 AM ET on October 12, 2026.", "Madrid, Spain",
         "2026-10-12 00:00", "America/New_York", "2026-10-12 06:00"),
    Case("sem-2", "wording", "Papers are due October 9, 2026 (23:59 AoE).", "Madrid, Spain",
         "2026-10-09 23:59", "-12:00", "2026-10-10 13:59"),
    Case("sem-3", "wording", "Registration closes 12:00 PM PT, August 14, 2026.", "Madrid, Spain",
         "2026-08-14 12:00", "America/Los_Angeles", "2026-08-14 21:00"),
    # Non-hour offsets and southern-hemisphere summer time (Australia moves clocks forward on Oct 4, 2026).
    Case("off-1", "offsets", "Deadline: 11:59 PM IST, November 10, 2026.", "Madrid, Spain",
         "2026-11-10 23:59", "+05:30", "2026-11-10 19:29"),
    Case("off-2", "offsets", "Submissions close at 5:00 PM Nepal time on April 2, 2026.", "Lima, Peru",
         "2026-04-02 17:00", "+05:45", "2026-04-02 06:15"),
    Case("off-3", "offsets", "Applications close 10:00 AM Adelaide time, October 6, 2026.", "Madrid, Spain",
         "2026-10-06 10:00", "Australia/Adelaide", "2026-10-06 01:30"),
    Case("off-4", "offsets", "Entries close 6:00 PM Sydney time on October 3, 2026.", "Madrid, Spain",
         "2026-10-03 18:00", "Australia/Sydney", "2026-10-03 10:00"),
]


CASES_HARD = [
    # Relative dates: the day has to be worked out from "today".
    Case("h-rel-1", "relative-date",
         "Today is Saturday, October 24, 2026. Submissions close six days from today, on Friday, at 11:59 PM PT.",
         "Madrid, Spain", "2026-10-30 23:59", "America/Los_Angeles", "2026-10-31 07:59"),
    Case("h-rel-2", "relative-date",
         "Today is Friday, October 30, 2026. The form closes this coming Monday at 10:00 AM Los Angeles time.",
         "Madrid, Spain", "2026-11-02 10:00", "America/Los_Angeles", "2026-11-02 19:00"),
    # Durations in absolute time that cross a clock change.
    Case("h-dur-1", "duration",
         "The hackathon starts Saturday, October 24, 2026 at 18:00 Madrid time and lasts exactly 48 hours.",
         "Madrid, Spain", "2026-10-24 18:00", "Europe/Madrid", "2026-10-26 17:00", shift_minutes=48 * 60,
         target="the end of the hackathon"),
    Case("h-dur-2", "duration",
         "The final round starts October 26, 2026 at 10:00 AM PT; submissions close exactly 72 hours later.",
         "Madrid, Spain", "2026-10-26 10:00", "America/Los_Angeles", "2026-10-29 18:00", shift_minutes=72 * 60),
    Case("h-dur-3", "duration",
         "Submissions close October 31, 2026 at 11:59 PM ET. Results are announced exactly 36 hours after "
         "submissions close.",
         "Madrid, Spain", "2026-10-31 23:59", "America/New_York", "2026-11-02 16:59", shift_minutes=36 * 60,
         target="the results announcement"),
    # Machine formats.
    Case("h-fmt-1", "machine-format", "Deadline (Unix timestamp, seconds): 1791788340.",
         "Tokyo, Japan", "1970-01-01 00:00", "+00:00", "2026-10-12 15:59", shift_minutes=1791788340 // 60),
    Case("h-fmt-2", "machine-format", "Deadline: 2026-10-25T02:30:00Z.",
         "Madrid, Spain", "2026-10-25 02:30", "+00:00", "2026-10-25 03:30"),
    # Dates described rather than written.
    Case("h-desc-1", "described-date",
         "Entries close at 11:59 PM Pacific Time on the last Sunday of October 2026.",
         "Madrid, Spain", "2026-10-25 23:59", "America/Los_Angeles", "2026-10-26 07:59"),
    Case("h-desc-2", "described-date",
         "Deadline: 12:00 noon Eastern Time on the day the US ends daylight saving time in 2026.",
         "Lima, Peru", "2026-11-01 12:00", "America/New_York", "2026-11-01 12:00"),
    Case("h-desc-3", "described-date", "Deadline: December 31, 2026, 24:00 AoE.",
         "Tokyo, Japan", "2027-01-01 00:00", "-12:00", "2027-01-01 21:00"),
    # The reader is not where they live.
    Case("h-trav-1", "traveling", "The deadline is 5:00 PM Sydney time on October 5, 2026.",
         "Madrid, Spain, but that week I'm traveling in New York, USA, and I need New York time",
         "2026-10-05 17:00", "Australia/Sydney", "2026-10-05 02:00"),
]

def _zone(spec: str):
    if spec[0] in "+-":
        sign = 1 if spec[0] == "+" else -1
        hours, minutes = map(int, spec[1:].split(":"))
        return timezone(sign * timedelta(hours=hours, minutes=minutes))
    return ZoneInfo(spec)


# Paired confirmatory set (pre-registered in docs/04-PREREGISTRO.md before any run). Every trap case has a control
# twin with the same wording, reader, clock time and weekday; only the date moves out of the period where the usual
# offset does not hold (the EU/US gap weeks, or a duration that crosses a clock change).
_FMT = "%Y-%m-%d %H:%M"
_CONVERSIONS = [  # (label in the text, source zone, reader)
    ("PT", "America/Los_Angeles", "Madrid, Spain"),
    ("ET", "America/New_York", "London, UK"),
    ("ET", "America/New_York", "Madrid, Spain"),
    ("PT", "America/Los_Angeles", "London, UK"),
    ("Berlin time", "Europe/Berlin", "New York, USA"),
    ("London time", "Europe/London", "Los Angeles, USA"),
]
_DURATIONS = [  # (city in the text, zone, reader living there)
    ("Madrid", "Europe/Madrid", "Madrid, Spain"),
    ("London", "Europe/London", "London, UK"),
    ("New York", "America/New_York", "New York, USA"),
    ("Los Angeles", "America/Los_Angeles", "Los Angeles, USA"),
]
# Day before each 2026 clock change in the zone of a duration event: EU on Mar 29 and Oct 25, US on Mar 8 and Nov 1.
_CHANGE_DAY = {"autumn": {"EU": "2026-10-25", "US": "2026-11-01"}, "spring": {"EU": "2026-03-29", "US": "2026-03-08"}}


def _clock(local: datetime) -> str:
    return local.strftime("%I:%M %p").lstrip("0")


def _long_date(local: datetime) -> str:
    return f"{local:%A}, {local:%B} {local.day}, 2026"


def _offset(zone: str, local: datetime) -> timedelta:
    return local.replace(tzinfo=ZoneInfo(zone)).utcoffset()


def _convert(local: datetime, source: str, reader: str) -> str:
    instant = local.replace(tzinfo=ZoneInfo(source)).astimezone(timezone.utc)
    return instant.astimezone(ZoneInfo(READERS[reader])).strftime(_FMT)


def _conversion_pairs() -> list[Case]:
    cases = []
    plan = [("autumn", ["11:59 PM", "9:00 AM", "5:00 PM"], datetime(2026, 10, 26), -7),
            ("spring", ["11:59 PM", "8:00 AM"], datetime(2026, 3, 9), 21)]
    n = 0
    for season, clocks, first_trap_day, control_shift in plan:
        for i, (label, source, reader) in enumerate(_CONVERSIONS):
            for j, clock in enumerate(clocks):
                n += 1
                day = first_trap_day + timedelta(days=(i * len(clocks) + j) % 6)  # Monday to Saturday
                time_ = datetime.strptime(clock, "%I:%M %p")
                trap = day.replace(hour=time_.hour, minute=time_.minute)
                control = trap + timedelta(days=control_shift)
                usual = (_offset(READERS[reader], datetime(2026, 7, 1, 12)) - _offset(source, datetime(2026, 7, 1, 12)))
                for role, local in (("trap", trap), ("control", control)):
                    gap = _offset(READERS[reader], local) - _offset(source, local)
                    expected = _convert(local, source, reader)
                    naive = (local + usual).strftime(_FMT)
                    assert (gap != usual) == (role == "trap"), (season, label, reader, role, local)
                    assert (naive != expected) == (role == "trap"), (season, label, reader, role, local)
                    cases.append(Case(
                        f"pc-{season[:3]}-{n:02d}-{role[0].upper()}", f"pair-conversion-{season}-{role}",
                        f"Submissions close {_long_date(local)} at {_clock(local)} {label}.", reader,
                        local.strftime(_FMT), source, expected, naive=naive))
    return cases


def _duration_pairs() -> list[Case]:
    cases = []
    # (season, hours, start weekday offset from the change day, start clock)
    plan = [("autumn", 24, -1, "6:00 PM"), ("autumn", 48, -2, "6:00 PM"), ("autumn", 72, -3, "8:00 PM"),
            ("spring", 24, -1, "12:00 PM"), ("spring", 48, -2, "6:00 PM")]
    n = 0
    for season, hours, start_offset, clock in plan:
        for city, zone, reader in _DURATIONS:
            n += 1
            change = datetime.strptime(_CHANGE_DAY[season]["EU" if zone.startswith("Europe") else "US"], "%Y-%m-%d")
            time_ = datetime.strptime(clock, "%I:%M %p")
            trap = (change + timedelta(days=start_offset)).replace(hour=time_.hour, minute=time_.minute)
            for role, local in (("trap", trap), ("control", trap - timedelta(days=7))):
                end = local.replace(tzinfo=ZoneInfo(zone)).astimezone(timezone.utc) + timedelta(hours=hours)
                expected = end.astimezone(ZoneInfo(zone)).strftime(_FMT)
                naive = (local + timedelta(hours=hours)).strftime(_FMT)  # adding clock hours
                assert (naive != expected) == (role == "trap"), (season, city, hours, role, local)
                cases.append(Case(
                    f"pd-{season[:3]}-{n:02d}-{role[0].upper()}", f"pair-duration-{season}-{role}",
                    f"The hackathon starts {_long_date(local)} at {_clock(local)} {city} time and lasts exactly "
                    f"{hours} hours.", reader, local.strftime(_FMT), zone, expected,
                    shift_minutes=hours * 60, target="the end of the hackathon", naive=naive))
    return cases


CASES_PAIRS = _conversion_pairs() + _duration_pairs()
CASE_SETS = {"standard": CASES, "hard": CASES_HARD, "pairs": CASES_PAIRS}
ALL_CASES = CASES + CASES_HARD + CASES_PAIRS


def computed_answer(case: Case) -> str:
    source = datetime.strptime(case.source_local, "%Y-%m-%d %H:%M").replace(tzinfo=_zone(case.source_zone))
    # Convert to UTC first, then add: with ZoneInfo, "aware datetime + timedelta" adds wall-clock time and ignores
    # the clock change (48 h from Oct 24, 18:00 in Madrid would give 18:00 instead of 17:00).
    source = source.astimezone(timezone.utc) + timedelta(minutes=case.shift_minutes)
    return source.astimezone(ZoneInfo(READERS[case.reader])).strftime("%Y-%m-%d %H:%M")


_mismatches = [(c.id, c.expected, computed_answer(c)) for c in ALL_CASES if c.expected != computed_answer(c)]
assert not _mismatches, f"Hand-written answer differs from the computed one: {_mismatches}"
assert len({c.id for c in ALL_CASES}) == len(ALL_CASES), "duplicate case ids"

PROMPTS = {
    # Free reasoning, as in an unhurried conversation.
    "reasoned": (
        "I live in {reader}. A contest page says: \"{statement}\"\n"
        "When is {target} in my local time? You may reason briefly, but end your reply with one final line "
        "exactly in this format: ANSWER: YYYY-MM-DD HH:MM (24-hour clock, my local time)."
    ),
    # The answer only, as in a quick lookup or an agent writing the deadline into a calendar.
    "direct": (
        "I live in {reader}. A contest page says: \"{statement}\"\n"
        "When is {target} in my local time? Reply with exactly one line and nothing else: "
        "ANSWER: YYYY-MM-DD HH:MM (24-hour clock, my local time)."
    ),
}
ANSWER_RE = re.compile(r"ANSWER:\s*\**\s*(\d{4}-\d{2}-\d{2})[ T](\d{1,2}):(\d{2})")


def parse_answer(text: str) -> str | None:
    matches = ANSWER_RE.findall(text or "")
    if not matches:
        return None
    day, hour, minute = matches[-1]
    return f"{day} {int(hour):02d}:{minute}"


# Mode and case set of the task pushed to Kaggle; `construir_kaggle.py` writes one file per combination by
# rewriting these two lines.
MODE = "reasoned"
SET = "pairs"  # "hard" for the exploratory set

# Kaggle reserves the maximum possible cost of each call from the output limit: without a limit, expensive models
# do not fit in the quota. The local pilot peaked at ~6,400 output tokens (standard) and ~18,700 (hard, reasoning).
MAX_TOKENS = 16384 if SET == "hard" else 8192


def ask(llm, case: Case) -> tuple[str, int]:
    """One call with retries, each in a fresh chat (otherwise the prompt would repeat inside the conversation).

    Returns the reply and its output tokens, to tell whether it was cut off at MAX_TOKENS.

    Open models often return 429 ("heavy load"). If a case runs out of retries the whole run fails visibly: an
    API error is not a wrong answer and must not be scored as one.
    """
    prompt = PROMPTS[MODE].format(reader=case.reader, statement=case.statement, target=case.target)
    for attempt in range(4):
        try:
            with kbench.chats.new(f"{case.id}-try{attempt + 1}") as chat:
                response = llm.prompt(prompt, extra_api_params={"max_tokens": MAX_TOKENS})
                return response, chat.usage.output_tokens or 0
        except Exception as error:
            last_error = error
            print(f"{case.id}: attempt {attempt + 1} failed: {error}", flush=True)
            time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"{case.id}: no answer after 4 attempts (API error, not a wrong answer): {last_error}")


@kbench.task(
    name="deadline-math-pairs-reasoned",
    # Must be a literal of at most 255 characters, or Kaggle rejects the task.
    description='Pre-registered paired set, reasoning allowed. 50 trap/control pairs: the same deadline inside and outside the weeks when the EU and US change clocks on different dates, and durations that do or do not cross a clock change. Ground truth from zoneinfo.',
)
def deadline_math(llm) -> float:
    passed = 0
    for case in CASE_SETS[SET]:
        response, output_tokens = ask(llm, case)
        answer = parse_answer(response)
        # No answer line and close to the limit: the reply was cut off. Scored as a failure, but flagged.
        truncated = answer is None and output_tokens >= 0.95 * MAX_TOKENS
        kbench.assertions.assert_equal(
            case.expected, answer,
            expectation=f"[{case.category}] {case.id}: {case.statement} -> {case.reader} = {case.expected}"
            + (f" (truncated at max_tokens={MAX_TOKENS})" if truncated else ""),
        )
        passed += answer == case.expected
    # Share of correct answers: Kaggle does not support "passed of total" yet (it reads a tuple as value ± CI).
    return passed / len(CASE_SETS[SET])


if __name__ == "__main__":
    deadline_math.run(kbench.llm)
