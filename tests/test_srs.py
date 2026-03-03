import unittest
from datetime import date

from immuno_study.store import SRSState, due_card_ids, update_srs


class TestSRS(unittest.TestCase):
    def test_update_srs_correct_increases_interval(self) -> None:
        srs: dict[str, dict[str, SRSState]] = {}
        deck = "deck.json"
        cid = "c1"
        today = date(2026, 1, 26)
        st1 = update_srs(srs=srs, deck_path=deck, card_id=cid, correct=True, today=today)
        self.assertEqual(st1.interval_days, 1)
        self.assertGreaterEqual(st1.due, today)

        first_due = st1.due  # 注意：update_srs 会原地更新同一个 state 对象
        st2 = update_srs(srs=srs, deck_path=deck, card_id=cid, correct=True, today=first_due)
        self.assertGreaterEqual(st2.interval_days, 1)
        self.assertGreater(st2.due, first_due)

    def test_due_card_ids(self) -> None:
        deck = "deck.json"
        today = date(2026, 1, 26)
        srs = {deck: {"a": SRSState(due=today), "b": SRSState(due=date(2026, 1, 27))}}
        due = due_card_ids(srs=srs, deck_path=deck, today=today)
        self.assertEqual(due, ["a"])

    def test_wrong_resets_interval(self) -> None:
        srs: dict[str, dict[str, SRSState]] = {}
        deck = "deck.json"
        cid = "c1"
        today = date(2026, 1, 26)
        update_srs(srs=srs, deck_path=deck, card_id=cid, correct=True, today=today)
        st = update_srs(srs=srs, deck_path=deck, card_id=cid, correct=False, today=today)
        self.assertEqual(st.interval_days, 1)
        self.assertEqual(st.streak, 0)


if __name__ == "__main__":
    unittest.main()

