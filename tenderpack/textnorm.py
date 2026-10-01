"""Normalisation for *matching only*. Source text is never replaced by its normalised form.

Latin normalisation (declared, minimal):
  NFKC (superscript digits become digits), typographic quotes -> ASCII quotes,
  en/em dashes and non-breaking hyphens -> '-', whitespace collapsed.
Arabic normalisation (for matching only; the printed form is kept in `source`):
  NFKC; remove tashkeel (U+064B-U+0652, U+0670) and tatweel (U+0640); unify alef forms
  (U+0622/0623/0625/0671 -> U+0627); Arabic-Indic and Extended Arabic-Indic digits -> ASCII.
  Letter shapes that change meaning (ta marbuta, alef maksura, ya) are NOT folded.
"""
from __future__ import annotations

import re
import unicodedata

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
_QUOTES = str.maketrans({"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"', "„": '"',
                         "–": "-", "—": "-", "‑": "-", "−": "-"})
_WS = re.compile(r"\s+")

ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"
EXT_ARABIC_INDIC = "۰۱۲۳۴۵۶۷۸۹"
_DIGITS = str.maketrans({**{c: str(i) for i, c in enumerate(ARABIC_INDIC)},
                         **{c: str(i) for i, c in enumerate(EXT_ARABIC_INDIC)}})
_TASHKEEL = re.compile("[ً-ْٰـ]")
_ALEF = str.maketrans({"آ": "ا", "أ": "ا", "إ": "ا", "ٱ": "ا"})


def normalize_latin(text: str) -> str:
    t = unicodedata.normalize("NFKC", text).translate(_QUOTES)
    return _WS.sub(" ", t).strip()


def normalize_arabic(text: str) -> str:
    t = unicodedata.normalize("NFKC", text)
    t = _TASHKEEL.sub("", t).translate(_ALEF).translate(_DIGITS).translate(_QUOTES)
    return _WS.sub(" ", t).strip()


def has_arabic(text: str) -> bool:
    return any("؀" <= ch <= "ۿ" or "ݐ" <= ch <= "ݿ" for ch in text)


def slug(text: str) -> str:
    t = normalize_latin(text).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "x"


def numerals(text: str) -> list[dict]:
    """Every run of digits (any script) with separators, in logical order."""
    out = []
    pattern = re.compile(r"[0-9٠-٩۰-۹](?:[0-9٠-٩۰-۹]|[.,\-/][0-9٠-٩۰-۹])*")
    for m in pattern.finditer(text):
        s = m.group(0)
        scripts = sorted({"arabic-indic" if c in ARABIC_INDIC else
                          "extended-arabic-indic" if c in EXT_ARABIC_INDIC else "ascii"
                          for c in s if c.isdigit()})
        out.append({"text": s, "start": m.start(), "scripts": scripts, "ascii": s.translate(_DIGITS)})
    return out
