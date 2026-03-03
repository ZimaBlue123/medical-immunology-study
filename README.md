# 医学免疫学学习工具（人卫《医学免疫学》第9版参考）

这是一个**离线、可追踪进度、可自测**的学习项目：用 Markdown 记录学习与复盘，用一个小型 Python CLI 做抽题自测、错题本与复习计划（间隔复习）。

> 说明：本项目**不包含教材原文**。大纲与题目均为“自写/概念化”内容，用于配合你手边的《医学免疫学》（人民卫生出版社，第9版）学习。

---

## 你能用它做什么

- **按模块学习**：`syllabus/outline.md` 给出免疫学学习模块清单与建议顺序
- **记录每次学习**：每次对话/学习创建一个会话笔记：`sessions/YYYY-MM-DD/session-notes.md`
- **跟踪总体进度**：统一在 `progress/immunology-study-tracker.md` 更新掌握情况与薄弱点
- **自测与复习**：
  - 从 `decks/*.json` 抽题做题
  - 自动记录本次分数、错题
  - 基于简单的间隔复习规则生成“今日应复习题目”

---

## 快速开始（Windows / PowerShell）

进入项目目录后：

```powershell
python -m immuno_study --help
python -m immuno_study quiz --deck .\decks\people9-core.json --n 10
python -m immuno_study review --deck .\decks\people9-core.json --n 10
python -m immuno_study stats
```

你也可以直接运行：

```powershell
python .\run_cli.py quiz --deck .\decks\people9-core.json --n 10
```

---

## 文档导航

- **完整使用指南（Web/CLI/数据存储说明）**：`docs/USER_GUIDE.md`
- **功能清单**：`docs/FEATURES.md`
- **知识库扩展记录**：`docs/knowledge-expansion-log.md`
- **Android 版本**：
  - 快速开始：`docs/android/ANDROID_QUICK_START.md`
  - 版本说明：`docs/android/ANDROID_README.md`
  - Android 工程入口：`android/README.md`

---

## 目录结构

```
medical-immunology-study/
  README.md
  CLAUDE.md
  syllabus/
    outline.md
  progress/
    immunology-study-tracker.md
  sessions/
    SESSION-TEMPLATE.md
    2026-01-26/
      session-notes.md   (你学习当天会生成/更新)
  decks/
    people9-core.json    (示例题库，可自行扩充)
  immuno_study/
    cli.py               (命令行入口)
    deck.py              (题库读写与校验)
    engine.py            (出题/判题)
    store.py             (学习记录、错题本、间隔复习状态)
    data/                (自动生成：attempts、srs、wrong_cards)
  tests/
    test_deck.py
    test_srs.py
  run_cli.py
```

---

## 如何把“教材第9版”融进来（推荐做法）

- **在 `syllabus/outline.md`**：把每个模块对应到你的教材章节/页码（你自己填写）
- **扩充题库**：复制 `decks/people9-core.json` 的题目结构，边学边加
  - 每题都写“为什么”解释（`explain`），并打标签（`tags`）方便按主题复习
- **每次学习后**：
  - 在 `sessions/YYYY-MM-DD/session-notes.md` 记录：学了什么、哪里卡住、错题原因
  - 在 `progress/immunology-study-tracker.md` 更新掌握度与薄弱点

---

## 运行测试（自我测试）

```powershell
python -m unittest discover -v -s .\tests
```

