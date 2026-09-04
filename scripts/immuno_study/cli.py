from __future__ import annotations

import argparse
import random
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from immuno_study.deck import DeckError, filter_cards, load_deck
from immuno_study.engine import grade_mcq, grade_short, letter_to_index
from immuno_study.store import (
    add_wrong_card,
    clear_wrong_card,
    due_card_ids,
    get_wrong_cards,
    load_srs,
    log_attempt,
    project_root,
    save_srs,
    summarize_attempts,
    update_srs,
)


def _wrap(s: str) -> str:
    return "\n".join(textwrap.wrap(s, width=88, replace_whitespace=False))


def _print_card_header(i: int, n: int, card: dict[str, Any]) -> None:
    tags = ", ".join(card.get("tags", []) or [])
    tag_part = f" [{tags}]" if tags else ""
    print(f"\n=== {i}/{n} | {card['id']} | {card['type']}{tag_part} ===")


def _ask_mcq(card: dict[str, Any]) -> tuple[bool, str]:
    print(_wrap(card["stem"]))
    choices = card["choices"]
    for idx, c in enumerate(choices):
        letter = chr(ord("A") + idx)
        print(f"  {letter}. {_wrap(c)}")

    start = time.time()
    while True:
        raw = input("你的答案（A/B/C/...，或直接回车跳过）> ").strip()
        if raw == "":
            return False, ""
        idx = letter_to_index(raw)
        if idx is None or not (0 <= idx < len(choices)):
            print("输入无效，请输入 A/B/C/... 或回车跳过。")
            continue
        ok = grade_mcq(card, idx)
        elapsed_ms = int((time.time() - start) * 1000)
        resp = chr(ord("A") + idx)
        return ok, f"{resp}|{elapsed_ms}"


def _ask_short(card: dict[str, Any]) -> tuple[bool, str]:
    print(_wrap(card["prompt"]))
    start = time.time()
    raw = input("你的答案（或回车跳过）> ")
    if raw.strip() == "":
        return False, ""
    ok = grade_short(card, raw)
    elapsed_ms = int((time.time() - start) * 1000)
    return ok, f"{raw.strip()}|{elapsed_ms}"


def _run_session(deck_path: str, cards: list[dict[str, Any]]) -> int:
    srs = load_srs()
    wrong_before = get_wrong_cards(deck_path)

    correct = 0
    total = len(cards)
    for i, card in enumerate(cards, start=1):
        _print_card_header(i, total, card)

        if card["type"] == "mcq":
            ok, resp = _ask_mcq(card)
        else:
            ok, resp = _ask_short(card)

        # resp 格式：text|elapsed_ms 或 ""（跳过）
        elapsed_ms = None
        response_text = resp
        if resp and "|" in resp:
            response_text, ms = resp.rsplit("|", 1)
            try:
                elapsed_ms = int(ms)
            except Exception:
                elapsed_ms = None

        if resp == "":
            print("已跳过。标准答案：")
            if card["type"] == "mcq":
                ai = card["answer_index"]
                print(f"  {chr(ord('A') + ai)}. {card['choices'][ai]}")
            else:
                print(f"  {card['answer']}")
            if card.get("explain"):
                print(_wrap(card["explain"]))
            continue

        if ok:
            correct += 1
            print("✅ 正确")
            clear_wrong_card(deck_path, card["id"])
        else:
            print("❌ 错误")
            add_wrong_card(deck_path, card["id"])

        update_srs(srs=srs, deck_path=deck_path, card_id=card["id"], correct=ok)
        save_srs(srs)

        log_attempt(
            deck_path=deck_path,
            card_id=card["id"],
            card_type=card["type"],
            correct=ok,
            response=response_text,
            elapsed_ms=elapsed_ms,
        )

        print("标准答案：")
        if card["type"] == "mcq":
            ai = card["answer_index"]
            print(f"  {chr(ord('A') + ai)}. {card['choices'][ai]}")
        else:
            print(f"  {card['answer']}")
        if card.get("explain"):
            print(_wrap(card["explain"]))

    wrong_after = get_wrong_cards(deck_path)
    newly_wrong = sorted(wrong_after - wrong_before)
    if newly_wrong:
        print("\n本次新增错题：", ", ".join(newly_wrong))

    acc = (correct / total) if total else 0.0
    print(f"\n本次成绩：{correct}/{total} = {acc:.0%}")
    return 0


def cmd_quiz(args: argparse.Namespace) -> int:
    deck_path = str(Path(args.deck).as_posix())
    deck = load_deck(args.deck)
    pool = filter_cards(deck.cards, args.tags)
    if not pool:
        print("没有符合 tags 过滤条件的题。")
        return 2
    n = min(args.n, len(pool))
    cards = random.sample(pool, k=n)
    return _run_session(deck_path, cards)


def cmd_review(args: argparse.Namespace) -> int:
    deck_path = str(Path(args.deck).as_posix())
    deck = load_deck(args.deck)
    srs = load_srs()
    due_ids = due_card_ids(srs=srs, deck_path=deck_path)

    by_id = {c["id"]: c for c in deck.cards}
    due_cards = [by_id[cid] for cid in due_ids if cid in by_id]

    if args.only_wrong:
        wrong = get_wrong_cards(deck_path)
        due_cards = [c for c in due_cards if c["id"] in wrong]

    if not due_cards:
        print("今天没有到期复习题。你可以改用 quiz 随机练习。")
        return 0

    n = min(args.n, len(due_cards))
    cards = due_cards[:n]
    return _run_session(deck_path, cards)


def cmd_stats(_: argparse.Namespace) -> int:
    s = summarize_attempts(last_n_days=7)
    print(f"累计做题记录：{s['total']}")
    if not s["by_day"]:
        print("近7天暂无做题记录。")
        return 0
    print("近7天：")
    for row in s["by_day"]:
        acc = row["accuracy"]
        acc_str = f"{acc:.0%}" if isinstance(acc, float) else "—"
        print(f"  {row['day']}: {row['correct']}/{row['count']} = {acc_str}")
    return 0


def cmd_new_session(_: argparse.Namespace) -> int:
    root = project_root()
    today = datetime.now().date().isoformat()
    session_dir = root / "sessions" / today
    session_dir.mkdir(parents=True, exist_ok=True)
    target = session_dir / "session-notes.md"
    if target.exists():
        print(f"已存在：{target}")
        return 0
    template = (root / "sessions" / "SESSION-TEMPLATE.md").read_text(encoding="utf-8")
    template = template.replace("[DATE]", today).replace("[YYYY-MM-DD]", today)
    target.write_text(template, encoding="utf-8")
    print(f"已生成：{target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="immuno_study", description="医学免疫学学习：自测、错题本、复习。")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("quiz", help="随机抽题练习")
    q.add_argument("--deck", required=True, help="题库路径（json）")
    q.add_argument("--n", type=int, default=10, help="题量（默认10）")
    q.add_argument("--tags", nargs="*", default=None, help="按标签过滤（任意命中）")
    q.set_defaults(func=cmd_quiz)

    r = sub.add_parser("review", help="按到期（SRS）复习")
    r.add_argument("--deck", required=True, help="题库路径（json）")
    r.add_argument("--n", type=int, default=10, help="题量（默认10）")
    r.add_argument("--only-wrong", action="store_true", help="只复习错题里到期的题")
    r.set_defaults(func=cmd_review)

    s = sub.add_parser("stats", help="查看做题统计（近7天）")
    s.set_defaults(func=cmd_stats)

    ns = sub.add_parser("new-session", help="为今天生成 sessions/YYYY-MM-DD/session-notes.md")
    ns.set_defaults(func=cmd_new_session)

    return p


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    p = build_parser()
    try:
        args = p.parse_args(argv)
        return int(args.func(args))
    except DeckError as e:
        print(f"题库格式错误：{e}")
        return 2

