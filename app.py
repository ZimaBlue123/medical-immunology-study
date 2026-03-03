"""
医学免疫学学习系统 - Web 应用（增强版）
Flask 后端，提供 API 接口
包含：学习教练、知识卡片、智能练习、学习进度
"""

from __future__ import annotations

import random
from pathlib import Path
from flask import Flask, jsonify, request, render_template

from immuno_study.deck import load_deck, filter_cards, DeckError
from immuno_study.engine import grade_mcq, grade_short, letter_to_index
from immuno_study.store import (
    load_srs,
    save_srs,
    update_srs,
    due_card_ids,
    get_wrong_cards,
    add_wrong_card,
    clear_wrong_card,
    log_attempt,
    summarize_attempts,
)
from immuno_study.knowledge import (
    KNOWLEDGE_BASE,
    MODULE_TAGS,
    get_module_knowledge,
    get_all_modules,
    get_concept_by_term,
    get_confusion_tips,
    analyze_wrong_answer,
    get_module_by_tag,
)

app = Flask(__name__, static_folder="static", template_folder="templates")

# 默认题库路径
DEFAULT_DECK = "decks/people9-core.json"


def get_deck_path() -> str:
    return request.args.get("deck", DEFAULT_DECK)


@app.route("/")
def index():
    """主页"""
    return render_template("index.html")


# ==================== 题库 API ====================

@app.route("/api/deck/info")
def api_deck_info():
    """获取题库信息"""
    try:
        deck_path = get_deck_path()
        deck = load_deck(deck_path)
        tags = set()
        for card in deck.cards:
            tags.update(card.get("tags", []))
        return jsonify({
            "success": True,
            "title": deck.title,
            "source": deck.source,
            "total_cards": len(deck.cards),
            "tags": sorted(tags),
        })
    except DeckError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except FileNotFoundError:
        return jsonify({"success": False, "error": "题库文件不存在"}), 404


# ==================== 练习 API ====================

@app.route("/api/quiz/start", methods=["POST"])
def api_quiz_start():
    """开始随机练习，返回题目列表"""
    try:
        data = request.get_json() or {}
        deck_path = data.get("deck", DEFAULT_DECK)
        n = int(data.get("n", 10))
        tags = data.get("tags")

        deck = load_deck(deck_path)
        pool = filter_cards(deck.cards, tags)

        if not pool:
            return jsonify({"success": False, "error": "没有符合条件的题目"}), 400

        n = min(n, len(pool))
        cards = random.sample(pool, k=n)

        quiz_cards = []
        for card in cards:
            c = {
                "id": card["id"],
                "type": card["type"],
                "tags": card.get("tags", []),
            }
            if card["type"] == "mcq":
                c["stem"] = card["stem"]
                c["choices"] = card["choices"]
            else:
                c["prompt"] = card["prompt"]
            quiz_cards.append(c)

        return jsonify({
            "success": True,
            "deck_path": deck_path,
            "total": len(quiz_cards),
            "cards": quiz_cards,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/quiz/submit", methods=["POST"])
def api_quiz_submit():
    """提交单题答案，返回批改结果（含学习引导）"""
    try:
        data = request.get_json() or {}
        deck_path = data.get("deck", DEFAULT_DECK)
        card_id = data.get("card_id")
        answer = data.get("answer")
        elapsed_ms = data.get("elapsed_ms")

        if not card_id:
            return jsonify({"success": False, "error": "缺少 card_id"}), 400

        deck = load_deck(deck_path)
        card = None
        for c in deck.cards:
            if c["id"] == card_id:
                card = c
                break

        if not card:
            return jsonify({"success": False, "error": "题目不存在"}), 404

        # 判题
        correct = False
        if card["type"] == "mcq":
            if answer:
                idx = letter_to_index(answer)
                if idx is not None:
                    correct = grade_mcq(card, idx)
        else:
            if answer:
                correct = grade_short(card, answer)

        # 更新 SRS
        srs = load_srs()
        update_srs(srs=srs, deck_path=deck_path, card_id=card_id, correct=correct)
        save_srs(srs)

        # 更新错题本
        if correct:
            clear_wrong_card(deck_path, card_id)
        else:
            add_wrong_card(deck_path, card_id)

        # 记录
        log_attempt(
            deck_path=deck_path,
            card_id=card_id,
            card_type=card["type"],
            correct=correct,
            response=answer or "",
            elapsed_ms=elapsed_ms,
        )

        # 构建结果
        result = {
            "success": True,
            "correct": correct,
            "explain": card.get("explain", ""),
        }
        
        if card["type"] == "mcq":
            ai = card["answer_index"]
            result["correct_answer"] = chr(ord("A") + ai)
            result["correct_text"] = card["choices"][ai]
        else:
            result["correct_answer"] = card["answer"]

        # 如果答错，提供学习引导
        if not correct:
            analysis = analyze_wrong_answer(card, answer or "")
            result["learning_guide"] = {
                "related_concepts": analysis["related_concepts"],
                "confusions": analysis["confusions"],
                "suggestions": analysis["suggestions"],
                "review_modules": analysis["review_modules"],
            }

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/review/cards", methods=["POST"])
def api_review_cards():
    """获取到期复习题"""
    try:
        data = request.get_json() or {}
        deck_path = data.get("deck", DEFAULT_DECK)
        n = int(data.get("n", 10))
        only_wrong = data.get("only_wrong", False)

        deck = load_deck(deck_path)
        srs = load_srs()
        due_ids = due_card_ids(srs=srs, deck_path=deck_path)

        by_id = {c["id"]: c for c in deck.cards}
        due_cards = [by_id[cid] for cid in due_ids if cid in by_id]

        if only_wrong:
            wrong = get_wrong_cards(deck_path)
            due_cards = [c for c in due_cards if c["id"] in wrong]

        n = min(n, len(due_cards))
        cards = due_cards[:n]

        quiz_cards = []
        for card in cards:
            c = {
                "id": card["id"],
                "type": card["type"],
                "tags": card.get("tags", []),
            }
            if card["type"] == "mcq":
                c["stem"] = card["stem"]
                c["choices"] = card["choices"]
            else:
                c["prompt"] = card["prompt"]
            quiz_cards.append(c)

        return jsonify({
            "success": True,
            "deck_path": deck_path,
            "total": len(quiz_cards),
            "due_total": len(due_ids),
            "cards": quiz_cards,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ==================== 统计 API ====================

@app.route("/api/stats")
def api_stats():
    """获取做题统计"""
    try:
        days = int(request.args.get("days", 7))
        stats = summarize_attempts(last_n_days=days)
        return jsonify({"success": True, **stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/wrong")
def api_wrong_cards():
    """获取错题列表"""
    try:
        deck_path = get_deck_path()
        wrong = get_wrong_cards(deck_path)
        return jsonify({
            "success": True,
            "deck_path": deck_path,
            "wrong_cards": sorted(wrong),
            "count": len(wrong),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ==================== 知识库 API ====================

@app.route("/api/knowledge/modules")
def api_knowledge_modules():
    """获取所有学习模块"""
    try:
        modules = get_all_modules()
        return jsonify({"success": True, "modules": modules})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/knowledge/module/<module_id>")
def api_knowledge_module(module_id: str):
    """获取指定模块的详细知识"""
    try:
        knowledge = get_module_knowledge(module_id)
        if not knowledge:
            return jsonify({"success": False, "error": "模块不存在"}), 404
        return jsonify({"success": True, "module": knowledge})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/knowledge/search")
def api_knowledge_search():
    """搜索知识点（支持多个结果）"""
    try:
        term = request.args.get("term", "")
        if not term:
            return jsonify({"success": False, "error": "请提供搜索词"}), 400
        
        # 使用search_concepts获取所有匹配结果
        from immuno_study.knowledge import search_concepts
        results = search_concepts(term)
        
        return jsonify({
            "success": True,
            "found": len(results) > 0,
            "count": len(results),
            "concepts": results[:20]  # 限制返回前20个结果
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/knowledge/concepts")
def api_knowledge_concepts():
    """获取所有知识点（可按模块筛选）"""
    try:
        module_id = request.args.get("module_id")
        
        all_concepts = []
        if module_id:
            # 获取指定模块的所有概念
            module_data = get_module_knowledge(module_id)
            if module_data:
                for concept in module_data.get("key_concepts", []):
                    all_concepts.append({
                        **concept,
                        "module": module_data["title"],
                        "module_id": module_id
                    })
        else:
            # 获取所有模块的所有概念
            for mid, module_data in KNOWLEDGE_BASE.items():
                for concept in module_data.get("key_concepts", []):
                    all_concepts.append({
                        **concept,
                        "module": module_data["title"],
                        "module_id": mid
                    })
        
        return jsonify({
            "success": True,
            "count": len(all_concepts),
            "concepts": all_concepts
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ==================== 学习教练 API ====================

@app.route("/api/coach/explore", methods=["POST"])
def api_coach_explore():
    """探测学习者对某个主题的理解（Socratic方法第一步）"""
    try:
        data = request.get_json() or {}
        topic = data.get("topic", "")
        
        if not topic:
            return jsonify({"success": False, "error": "请提供学习主题"}), 400
        
        # 查找相关模块
        related_module = None
        for module_id, tags in MODULE_TAGS.items():
            if topic.lower() in [t.lower() for t in tags] or topic.lower() in KNOWLEDGE_BASE[module_id]["title"].lower():
                related_module = module_id
                break
        
        # 生成探测问题
        questions = [
            f"你对「{topic}」目前的理解是什么？",
            f"你能举一个关于「{topic}」的例子吗？",
            f"你觉得「{topic}」和哪个概念容易混淆？"
        ]
        
        response = {
            "success": True,
            "topic": topic,
            "explore_questions": questions,
        }
        
        if related_module:
            module_data = KNOWLEDGE_BASE[related_module]
            response["related_module"] = {
                "id": related_module,
                "title": module_data["title"],
                "objectives": module_data["objectives"],
            }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/coach/explain", methods=["POST"])
def api_coach_explain():
    """根据学习者的基础给出聚焦解释"""
    try:
        data = request.get_json() or {}
        topic = data.get("topic", "")
        user_understanding = data.get("understanding", "")
        
        if not topic:
            return jsonify({"success": False, "error": "请提供学习主题"}), 400
        
        # 查找相关概念
        concept = get_concept_by_term(topic)
        
        # 查找相关模块
        related_module = None
        for module_id, tags in MODULE_TAGS.items():
            if topic.lower() in [t.lower() for t in tags]:
                related_module = module_id
                break
        
        explanation = {
            "success": True,
            "topic": topic,
        }
        
        if concept:
            explanation["concept"] = concept
            explanation["structure"] = {
                "definition": concept["definition"],
                "key_points": concept["key_points"],
                "memory_tip": concept.get("memory_tip", ""),
            }
        
        if related_module:
            module_data = KNOWLEDGE_BASE[related_module]
            explanation["confusions"] = module_data.get("confusions", [])[:2]
            explanation["clinical_links"] = module_data.get("clinical_links", [])[:2]
        
        # 生成检验问题
        explanation["check_questions"] = [
            f"你能用自己的话解释「{topic}」吗？",
            f"如果考试问到「{topic}」，你会从哪几个角度回答？",
        ]
        
        return jsonify(explanation)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/coach/quiz-topic", methods=["POST"])
def api_coach_quiz_topic():
    """获取特定主题的练习题"""
    try:
        data = request.get_json() or {}
        topic = data.get("topic", "")
        n = int(data.get("n", 3))
        
        if not topic:
            return jsonify({"success": False, "error": "请提供主题"}), 400
        
        deck = load_deck(DEFAULT_DECK)
        
        # 根据主题筛选题目
        matching_cards = []
        topic_lower = topic.lower()
        for card in deck.cards:
            card_tags = [t.lower() for t in card.get("tags", [])]
            if topic_lower in card_tags or any(topic_lower in t for t in card_tags):
                matching_cards.append(card)
        
        if not matching_cards:
            return jsonify({"success": False, "error": "没有找到相关题目"}), 404
        
        n = min(n, len(matching_cards))
        selected = random.sample(matching_cards, k=n)
        
        quiz_cards = []
        for card in selected:
            c = {
                "id": card["id"],
                "type": card["type"],
                "tags": card.get("tags", []),
            }
            if card["type"] == "mcq":
                c["stem"] = card["stem"]
                c["choices"] = card["choices"]
            else:
                c["prompt"] = card["prompt"]
            quiz_cards.append(c)
        
        return jsonify({
            "success": True,
            "topic": topic,
            "cards": quiz_cards,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# ==================== 学习进度 API ====================

@app.route("/api/progress/overview")
def api_progress_overview():
    """获取学习进度概览"""
    try:
        deck_path = get_deck_path()
        deck = load_deck(deck_path)
        srs = load_srs()
        wrong = get_wrong_cards(deck_path)
        stats = summarize_attempts(last_n_days=7)
        
        # 计算各模块进度
        module_progress = {}
        for module_id in KNOWLEDGE_BASE.keys():
            module_tags = MODULE_TAGS.get(module_id, [])
            module_cards = [c for c in deck.cards if any(t in c.get("tags", []) for t in module_tags)]
            
            practiced = 0
            mastered = 0
            deck_srs = srs.get(deck_path, {})
            
            for card in module_cards:
                card_srs = deck_srs.get(card["id"])
                if card_srs:
                    practiced += 1
                    if card_srs.interval_days >= 7 and card["id"] not in wrong:
                        mastered += 1
            
            module_progress[module_id] = {
                "title": KNOWLEDGE_BASE[module_id]["title"],
                "total": len(module_cards),
                "practiced": practiced,
                "mastered": mastered,
                "progress": round(practiced / len(module_cards) * 100) if module_cards else 0,
            }
        
        return jsonify({
            "success": True,
            "total_cards": len(deck.cards),
            "wrong_count": len(wrong),
            "stats": stats,
            "module_progress": module_progress,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    print("=" * 50)
    print("   Medical Immunology Study System")
    print("   Yi Xue Mian Yi Xue Xue Xi Xi Tong")
    print("=" * 50)
    print("Visit http://127.0.0.1:5000 to start learning")
    print("=" * 50)
    app.run(debug=True, port=5000)
