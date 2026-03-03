from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def project_root() -> Path:
    # .../medical-immunology-study/immuno_study/store.py -> project root is parents[1]
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    p = Path(__file__).resolve().parent / "data"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _json_load(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _json_save(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def attempts_path() -> Path:
    # jsonl 便于追加
    return data_dir() / "attempts.jsonl"


def log_attempt(
    *,
    deck_path: str,
    card_id: str,
    card_type: str,
    correct: bool,
    response: str,
    elapsed_ms: int | None = None,
) -> None:
    rec = {
        "ts_utc": _utcnow().isoformat(),
        "deck": deck_path,
        "card_id": card_id,
        "card_type": card_type,
        "correct": bool(correct),
        "response": response,
        "elapsed_ms": elapsed_ms,
    }
    p = attempts_path()
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def wrong_cards_path() -> Path:
    return data_dir() / "wrong_cards.json"


def add_wrong_card(deck_path: str, card_id: str) -> None:
    p = wrong_cards_path()
    data: dict[str, list[str]] = _json_load(p, default={})
    cur = set(data.get(deck_path, []))
    cur.add(card_id)
    data[deck_path] = sorted(cur)
    _json_save(p, data)


def clear_wrong_card(deck_path: str, card_id: str) -> None:
    p = wrong_cards_path()
    data: dict[str, list[str]] = _json_load(p, default={})
    cur = set(data.get(deck_path, []))
    if card_id in cur:
        cur.remove(card_id)
        data[deck_path] = sorted(cur)
        _json_save(p, data)


def get_wrong_cards(deck_path: str) -> set[str]:
    data: dict[str, list[str]] = _json_load(wrong_cards_path(), default={})
    return set(data.get(deck_path, []))


@dataclass
class SRSState:
    ease: float = 2.3
    interval_days: int = 0
    due: date = date.today()
    last_review: date | None = None
    streak: int = 0


def srs_path() -> Path:
    return data_dir() / "srs.json"


def _state_to_dict(s: SRSState) -> dict[str, Any]:
    return {
        "ease": s.ease,
        "interval_days": s.interval_days,
        "due": s.due.isoformat(),
        "last_review": s.last_review.isoformat() if s.last_review else None,
        "streak": s.streak,
    }


def _dict_to_state(d: dict[str, Any]) -> SRSState:
    due = date.fromisoformat(d.get("due") or date.today().isoformat())
    lr = d.get("last_review")
    last_review = date.fromisoformat(lr) if isinstance(lr, str) else None
    ease = float(d.get("ease", 2.3))
    interval_days = int(d.get("interval_days", 0))
    streak = int(d.get("streak", 0))
    return SRSState(ease=ease, interval_days=interval_days, due=due, last_review=last_review, streak=streak)


def load_srs() -> dict[str, dict[str, SRSState]]:
    raw: dict[str, dict[str, Any]] = _json_load(srs_path(), default={})
    out: dict[str, dict[str, SRSState]] = {}
    for deck, per in raw.items():
        out[deck] = {cid: _dict_to_state(st) for cid, st in (per or {}).items()}
    return out


def save_srs(srs: dict[str, dict[str, SRSState]]) -> None:
    raw: dict[str, dict[str, Any]] = {}
    for deck, per in srs.items():
        raw[deck] = {cid: _state_to_dict(st) for cid, st in per.items()}
    _json_save(srs_path(), raw)


def update_srs(
    *,
    srs: dict[str, dict[str, SRSState]],
    deck_path: str,
    card_id: str,
    correct: bool,
    today: date | None = None,
) -> SRSState:
    """
    轻量 SRS（不追求完美 SM-2，追求可用）：
    - 答对：streak+1，interval = max(1, round(interval * ease))，ease 小幅上调
    - 答错：streak=0，interval=1，ease 下调（最低 1.3）
    - due = today + interval_days
    """
    if today is None:
        today = datetime.now().date()

    per = srs.setdefault(deck_path, {})
    st = per.get(card_id, SRSState(due=today))

    if correct:
        st.streak += 1
        st.ease = min(3.0, st.ease + 0.05)
        if st.interval_days <= 0:
            st.interval_days = 1
        else:
            st.interval_days = max(1, int(round(st.interval_days * st.ease)))
    else:
        st.streak = 0
        st.ease = max(1.3, st.ease - 0.2)
        st.interval_days = 1

    st.last_review = today
    st.due = today + timedelta(days=st.interval_days)
    per[card_id] = st
    return st


def due_card_ids(
    *,
    srs: dict[str, dict[str, SRSState]],
    deck_path: str,
    today: date | None = None,
) -> list[str]:
    if today is None:
        today = datetime.now().date()
    per = srs.get(deck_path, {})
    due = [cid for cid, st in per.items() if st.due <= today]
    return sorted(due)


def summarize_attempts(last_n_days: int = 7) -> dict[str, Any]:
    p = attempts_path()
    if not p.exists():
        return {"total": 0, "last_n_days": last_n_days, "by_day": []}

    cutoff = datetime.now(timezone.utc) - timedelta(days=last_n_days)
    by_day: dict[str, list[bool]] = {}
    total = 0
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            total += 1
            ts = rec.get("ts_utc")
            try:
                dt = datetime.fromisoformat(ts)
            except Exception:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt < cutoff:
                continue
            day = dt.date().isoformat()
            by_day.setdefault(day, []).append(bool(rec.get("correct")))

    out = []
    for day in sorted(by_day.keys()):
        vals = by_day[day]
        out.append(
            {
                "day": day,
                "count": len(vals),
                "correct": sum(1 for v in vals if v),
                "accuracy": (sum(1 for v in vals if v) / len(vals)) if vals else None,
            }
        )
    return {"total": total, "last_n_days": last_n_days, "by_day": out}

