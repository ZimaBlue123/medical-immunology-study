#!/usr/bin/env python3
"""
将Python数据转换为Android JavaScript文件
"""
import json
import os
from pathlib import Path

# 导入知识库和题库
from immuno_study.knowledge import KNOWLEDGE_BASE, MODULE_TAGS
from immuno_study.deck import load_deck

def convert_knowledge_base():
    """转换知识库为JavaScript"""
    js_content = "// 医学免疫学知识库\n"
    js_content += "// 自动生成，请勿手动修改\n\n"
    js_content += "const KNOWLEDGE_BASE = " + json.dumps(KNOWLEDGE_BASE, ensure_ascii=False, indent=2) + ";\n\n"
    js_content += "const MODULE_TAGS = " + json.dumps(MODULE_TAGS, ensure_ascii=False, indent=2) + ";\n\n"
    
    # 添加辅助函数
    js_content += """
// 辅助函数
function getModuleKnowledge(moduleId) {
    return KNOWLEDGE_BASE[moduleId] || null;
}

function getAllModules() {
    return Object.keys(KNOWLEDGE_BASE).map(id => ({
        id: id,
        title: KNOWLEDGE_BASE[id].title,
        objectives: KNOWLEDGE_BASE[id].objectives
    }));
}

function getConceptByTerm(term) {
    const termLower = term.toLowerCase();
    for (const [moduleId, moduleData] of Object.entries(KNOWLEDGE_BASE)) {
        for (const concept of moduleData.key_concepts || []) {
            if (concept.term.toLowerCase().includes(termLower)) {
                return {
                    ...concept,
                    module: moduleData.title,
                    module_id: moduleId
                };
            }
        }
    }
    return null;
}

function searchConcepts(query) {
    const queryLower = query.toLowerCase();
    const results = [];
    for (const [moduleId, moduleData] of Object.entries(KNOWLEDGE_BASE)) {
        for (const concept of moduleData.key_concepts || []) {
            if (concept.term.toLowerCase().includes(queryLower) || 
                concept.definition.toLowerCase().includes(queryLower)) {
                results.push({
                    ...concept,
                    module: moduleData.title,
                    module_id: moduleId
                });
            }
        }
    }
    return results;
}

function getModuleByTag(tag) {
    const tagLower = tag.toLowerCase();
    for (const [moduleId, tags] of Object.entries(MODULE_TAGS)) {
        if (tags.some(t => t.toLowerCase() === tagLower)) {
            return moduleId;
        }
    }
    return null;
}
"""
    
    return js_content

def convert_deck():
    """转换题库为JavaScript"""
    deck = load_deck("decks/people9-core.json")
    
    js_content = "// 医学免疫学题库\n"
    js_content += "// 自动生成，请勿手动修改\n\n"
    js_content += "const DECK_DATA = " + json.dumps({
        "meta": {
            "title": deck.title,
            "source": deck.source,
            "version": deck.version
        },
        "cards": deck.cards
    }, ensure_ascii=False, indent=2) + ";\n\n"
    
    js_content += """
function getDeckCards() {
    return DECK_DATA.cards || [];
}

function getCardById(cardId) {
    return DECK_DATA.cards.find(c => c.id === cardId) || null;
}

function filterCardsByTags(cards, tags) {
    if (!tags || tags.length === 0) return cards;
    return cards.filter(card => {
        const cardTags = card.tags || [];
        return tags.some(tag => cardTags.includes(tag));
    });
}
"""
    
    return js_content

def main():
    """主函数"""
    # 创建输出目录
    output_dir = Path("android/app/src/main/assets/js")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 转换知识库
    print("Converting knowledge base...")
    kb_js = convert_knowledge_base()
    kb_file = output_dir / "knowledge-base.js"
    with open(kb_file, "w", encoding="utf-8") as f:
        f.write(kb_js)
    print(f"Generated: {kb_file}")
    
    # 转换题库
    print("Converting deck data...")
    deck_js = convert_deck()
    deck_file = output_dir / "deck-data.js"
    with open(deck_file, "w", encoding="utf-8") as f:
        f.write(deck_js)
    print(f"Generated: {deck_file}")
    
    print("\nConversion complete!")

if __name__ == "__main__":
    main()
