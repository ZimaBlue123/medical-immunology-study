from __future__ import annotations

import re
from typing import Any


_WS_RE = re.compile(r"\s+")


def normalize_text(s: str | None) -> str:
    if not s or not isinstance(s, str):
        return ""
    return _WS_RE.sub(" ", s.strip().lower())


def grade_mcq(card: dict[str, Any], user_index: int | None) -> bool:
    if not isinstance(card, dict) or user_index is None:
        return False
    try:
        answer_index = card["answer_index"]
        return int(user_index) == int(answer_index)
    except (KeyError, ValueError, TypeError):
        return False


def grade_short(card: dict[str, Any], user_text: str | None) -> bool:
    if not isinstance(card, dict) or "answer" not in card or user_text is None:
        return False
    return normalize_text(user_text) == normalize_text(str(card["answer"]))


def letter_to_index(letter: str | None) -> int | None:
    if not letter or not isinstance(letter, str):
        return None
    s = letter.strip().upper()
    if len(s) == 1 and "A" <= s <= "Z":
        return ord(s) - ord("A")
    return None


def index_to_letter(index: int | None) -> str:
    if index is None or not isinstance(index, int) or not (0 <= index <= 25):
        return ""
    return chr(ord("A") + index)

