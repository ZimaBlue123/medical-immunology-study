import unittest
from pathlib import Path

from immuno_study.deck import DeckError, load_deck, validate_deck_dict


class TestDeck(unittest.TestCase):
    def test_load_example_deck(self) -> None:
        root = Path(__file__).resolve().parents[1]
        deck_path = root / "decks" / "people9-core.json"
        deck = load_deck(deck_path)
        self.assertTrue(deck.title)
        self.assertGreaterEqual(len(deck.cards), 10)

    def test_reject_duplicate_id(self) -> None:
        bad = {
            "meta": {"title": "x", "source": "y", "version": 1},
            "cards": [
                {
                    "id": "dup",
                    "type": "short",
                    "prompt": "p",
                    "answer": "a",
                    "tags": ["t"],
                },
                {
                    "id": "dup",
                    "type": "short",
                    "prompt": "p2",
                    "answer": "a2",
                    "tags": ["t"],
                },
            ],
        }
        with self.assertRaises(DeckError):
            validate_deck_dict(bad)


if __name__ == "__main__":
    unittest.main()

