# Medical Immunology Study System

[中文](README.md) | [English](README.en.md)

An offline learning system for medical immunology (aligned with People's Medical Publishing House textbook framework): Web learning interface + CLI practice + SRS/wrong-answer tracking + session and progress documentation.

> Compliance note: this repository does not include copyrighted textbook text. Learning content is self-authored and concept-based.

## Deep Project Understanding

### 1) Product Positioning
- Designed for structured immunology learning with a practical workflow: concept building, frequent quizzes, wrong-answer review, and spaced repetition.
- Supports both browsing mode (knowledge cards/modules) and task mode (quiz/review/stats).

### 2) Technical Architecture
- **Backend**: `app.py` (Flask) exposing REST APIs for quiz, review, knowledge, coaching, and progress.
- **Core engine**: `immuno_study/deck.py`, `immuno_study/engine.py`, `immuno_study/store.py`.
- **Data layer**: local JSON/JSONL files, database-free, easy backup, offline-first.
- **Frontend**: native HTML/CSS/JS in `templates/` and static assets.
- **Android extension**: additional Android delivery artifacts under `android/`.

### 3) Learning Model
- **Knowledge model**: `immuno_study/knowledge.py` with 12 immunology modules.
- **Practice model**: `decks/people9-core.json` includes MCQ + short-answer cards with explanations and tags.
- **Memory model**: lightweight SRS with interval/ease/due date.
- **Coaching model**: Socratic flow (probe understanding -> focused explanation -> check questions).

### 4) Strengths and Improvement Opportunities
- **Strengths**: complete local workflow, strong traceability, practical study loop.
- **Possible upgrades**: short-answer grading can be enhanced from exact normalized matching to keyword/synonym/semantic scoring.

## Quick Start (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Web mode
python app.py
# Open http://127.0.0.1:5000
```

```powershell
# CLI mode
python -m immuno_study --help
python -m immuno_study quiz --deck .\decks\people9-core.json --n 10
python -m immuno_study review --deck .\decks\people9-core.json --n 10
python -m immuno_study stats
```

## Project Layout

```text
medical-immunology-study/
├─ app.py
├─ immuno_study/
├─ decks/
├─ docs/
├─ sessions/
├─ progress/
├─ android/
└─ tests/
```

## Recommended Learning Materials (Web Curated)

- NCBI Bookshelf: Immunobiology (Janeway entry, searchable access)  
  <https://www.ncbi.nlm.nih.gov/books/NBK10757/>
- WHO Essential Programme on Immunization (training hub)  
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/essential-programme-on-immunization/training>
- WHO General Immunization Training Materials  
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/essential-programme-on-immunization/training/general>
- CDC Pink Book (Epidemiology and Prevention of Vaccine-Preventable Diseases)  
  <https://www.cdc.gov/pinkbook/hcp/table-of-contents/index.html>
- AAI Teaching Resources  
  <https://www.aai.org/Education/Teaching-Resources>
- NIH Immune System Overview  
  <https://www.niaid.nih.gov/research/immune-system-overview>
- Khan Academy Immunology  
  <https://www.khanacademy.org/science/biology/immunology>

## How to Align with Your Main Textbook

- Map each module in `syllabus/outline.md` to your chapter/page references.
- Extend cards in `decks/people9-core.json` using existing schema (`id`, `type`, `tags`, `explain`).
- Keep daily notes and progress synchronized:
  - `sessions/YYYY-MM-DD/session-notes.md`
  - `progress/immunology-study-tracker.md`

## Tests

```powershell
python -m unittest discover -v -s .\tests
```

## License

Licensed under [Apache License 2.0](LICENSE).
