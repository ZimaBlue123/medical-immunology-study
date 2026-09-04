from __future__ import annotations

import re
from typing import Any


_WS_RE = re.compile(r"\s+")


def normalize_text(s: str) -> str:
    return _WS_RE.sub(" ", s.strip().lower())


def grade_mcq(card: dict[str, Any], user_index: int) -> bool:
    answer_index = card["answer_index"]
    return int(user_index) == int(answer_index)


def grade_short(card: dict[str, Any], user_text: str) -> bool:
    # 轻量策略：精确匹配归一化文本；你可以在题库里写“标准答案关键短句”
    return normalize_text(user_text) == normalize_text(card["answer"])


def letter_to_index(letter: str) -> int | None:
    s = letter.strip().upper()
    if not s:
        return None
    if len(s) == 1 and "A" <= s <= "Z":
        return ord(s) - ord("A")
    return None

