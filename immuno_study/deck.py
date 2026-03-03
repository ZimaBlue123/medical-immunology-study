from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Deck:
    title: str
    source: str
    version: int
    cards: list[dict[str, Any]]


class DeckError(ValueError):
    pass


def _require_str(obj: dict[str, Any], key: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v.strip():
        raise DeckError(f"Missing/invalid '{key}'")
    return v


def _require_int(obj: dict[str, Any], key: str) -> int:
    v = obj.get(key)
    if not isinstance(v, int):
        raise DeckError(f"Missing/invalid '{key}'")
    return v


def _require_list(obj: dict[str, Any], key: str) -> list[Any]:
    v = obj.get(key)
    if not isinstance(v, list):
        raise DeckError(f"Missing/invalid '{key}'")
    return v


def _validate_card(card: dict[str, Any]) -> None:
    _require_str(card, "id")
    ctype = _require_str(card, "type")

    tags = card.get("tags", [])
    if not isinstance(tags, list) or any((not isinstance(t, str) or not t.strip()) for t in tags):
        raise DeckError("Card 'tags' must be a list of non-empty strings")

    if ctype == "mcq":
        _require_str(card, "stem")
        choices = _require_list(card, "choices")
        if len(choices) < 2 or any((not isinstance(c, str) or not c.strip()) for c in choices):
            raise DeckError("MCQ 'choices' must be 2+ non-empty strings")
        ans = card.get("answer_index")
        if not isinstance(ans, int) or not (0 <= ans < len(choices)):
            raise DeckError("MCQ 'answer_index' must be a valid index")
        _require_str(card, "explain")
    elif ctype == "short":
        _require_str(card, "prompt")
        _require_str(card, "answer")
        exp = card.get("explain")
        if exp is not None and (not isinstance(exp, str)):
            raise DeckError("Short 'explain' must be a string when provided")
    else:
        raise DeckError(f"Unsupported card type: {ctype}")


def validate_deck_dict(data: dict[str, Any]) -> Deck:
    if not isinstance(data, dict):
        raise DeckError("Deck must be a JSON object")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        raise DeckError("Deck.meta must be an object")

    title = _require_str(meta, "title")
    source = _require_str(meta, "source")
    version = _require_int(meta, "version")

    cards = data.get("cards")
    if not isinstance(cards, list) or not cards:
        raise DeckError("Deck.cards must be a non-empty list")
    if any(not isinstance(c, dict) for c in cards):
        raise DeckError("Each card must be an object")

    seen: set[str] = set()
    for c in cards:
        _validate_card(c)
        cid = c["id"]
        if cid in seen:
            raise DeckError(f"Duplicate card id: {cid}")
        seen.add(cid)

    return Deck(title=title, source=source, version=version, cards=cards)


def load_deck(path: str | Path) -> Deck:
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    return validate_deck_dict(data)


def filter_cards(cards: Iterable[dict[str, Any]], tags: list[str] | None) -> list[dict[str, Any]]:
    cards_list = list(cards)
    if not tags:
        return cards_list
    wanted = {t.strip() for t in tags if t.strip()}
    if not wanted:
        return cards_list
    out: list[dict[str, Any]] = []
    for c in cards_list:
        ct = set(c.get("tags", []) or [])
        if ct & wanted:
            out.append(c)
    return out

