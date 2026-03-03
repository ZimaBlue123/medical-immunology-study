// 前端API层 - 替代Flask后端
// 使用localStorage存储学习数据

// ==================== 存储管理 ====================

const Storage = {
    // SRS数据
    getSRS() {
        const data = localStorage.getItem('srs');
        return data ? JSON.parse(data) : {};
    },
    
    saveSRS(srs) {
        localStorage.setItem('srs', JSON.stringify(srs));
    },
    
    // 错题本
    getWrongCards(deckPath) {
        const key = `wrong_cards_${deckPath}`;
        const data = localStorage.getItem(key);
        return data ? new Set(JSON.parse(data)) : new Set();
    },
    
    addWrongCard(deckPath, cardId) {
        const key = `wrong_cards_${deckPath}`;
        const wrong = this.getWrongCards(deckPath);
        wrong.add(cardId);
        localStorage.setItem(key, JSON.stringify(Array.from(wrong)));
    },
    
    clearWrongCard(deckPath, cardId) {
        const key = `wrong_cards_${deckPath}`;
        const wrong = this.getWrongCards(deckPath);
        wrong.delete(cardId);
        localStorage.setItem(key, JSON.stringify(Array.from(wrong)));
    },
    
    // 做题记录
    logAttempt(deckPath, cardId, cardType, correct, response, elapsedMs) {
        const key = 'attempts';
        const attempts = JSON.parse(localStorage.getItem(key) || '[]');
        attempts.push({
            deck_path: deckPath,
            card_id: cardId,
            card_type: cardType,
            correct: correct,
            response: response,
            elapsed_ms: elapsedMs,
            timestamp: new Date().toISOString()
        });
        // 只保留最近1000条记录
        if (attempts.length > 1000) {
            attempts.splice(0, attempts.length - 1000);
        }
        localStorage.setItem(key, JSON.stringify(attempts));
    },
    
    getAttempts() {
        return JSON.parse(localStorage.getItem('attempts') || '[]');
    }
};

// ==================== SRS算法 ====================

function updateSRS(srs, deckPath, cardId, correct) {
    if (!srs[deckPath]) {
        srs[deckPath] = {};
    }
    
    const cardSRS = srs[deckPath][cardId] || {
        ease_factor: 2.5,
        interval_days: 0,
        repetitions: 0,
        last_review: null
    };
    
    const now = new Date();
    
    if (correct) {
        if (cardSRS.repetitions === 0) {
            cardSRS.interval_days = 1;
        } else if (cardSRS.repetitions === 1) {
            cardSRS.interval_days = 6;
        } else {
            cardSRS.interval_days = Math.round(cardSRS.interval_days * cardSRS.ease_factor);
        }
        cardSRS.repetitions += 1;
        cardSRS.ease_factor = Math.max(1.3, cardSRS.ease_factor + 0.1);
    } else {
        cardSRS.repetitions = 0;
        cardSRS.interval_days = 0;
        cardSRS.ease_factor = Math.max(1.3, cardSRS.ease_factor - 0.2);
    }
    
    cardSRS.last_review = now.toISOString();
    srs[deckPath][cardId] = cardSRS;
}

function getDueCardIds(srs, deckPath) {
    const deckSRS = srs[deckPath] || {};
    const now = new Date();
    const due = [];
    
    for (const [cardId, cardSRS] of Object.entries(deckSRS)) {
        if (!cardSRS.last_review) {
            due.push(cardId);
            continue;
        }
        
        const lastReview = new Date(cardSRS.last_review);
        const daysSince = Math.floor((now - lastReview) / (1000 * 60 * 60 * 24));
        
        if (daysSince >= cardSRS.interval_days) {
            due.push(cardId);
        }
    }
    
    return due;
}

// ==================== 判题引擎 ====================

function gradeMCQ(card, answerIndex) {
    return card.answer_index === answerIndex;
}

function gradeShort(card, answer) {
    const correct = card.answer.toLowerCase().trim();
    const user = answer.toLowerCase().trim();
    
    // 简单匹配：包含关键词即可
    const keywords = correct.split(/[，,。.；;]/).filter(k => k.trim().length > 2);
    return keywords.some(k => user.includes(k.trim())) || user.includes(correct);
}

function letterToIndex(letter) {
    if (!letter || letter.length === 0) return null;
    const upper = letter.toUpperCase();
    if (upper >= 'A' && upper <= 'Z') {
        return upper.charCodeAt(0) - 'A'.charCodeAt(0);
    }
    return null;
}

// ==================== API接口 ====================

const API = {
    // 知识库API
    async getModules() {
        return {
            success: true,
            modules: getAllModules()
        };
    },
    
    async getModule(moduleId) {
        const module = getModuleKnowledge(moduleId);
        if (!module) {
            return { success: false, error: "模块不存在" };
        }
        return { success: true, module: module };
    },
    
    async searchKnowledge(term) {
        if (!term) {
            return { success: false, error: "请提供搜索词" };
        }
        const results = searchConcepts(term);
        return {
            success: true,
            found: results.length > 0,
            count: results.length,
            concepts: results.slice(0, 20)
        };
    },
    
    async getConcepts(moduleId) {
        let allConcepts = [];
        
        if (moduleId) {
            const module = getModuleKnowledge(moduleId);
            if (module) {
                for (const concept of module.key_concepts || []) {
                    allConcepts.push({
                        ...concept,
                        module: module.title,
                        module_id: moduleId
                    });
                }
            }
        } else {
            for (const [mid, module] of Object.entries(KNOWLEDGE_BASE)) {
                for (const concept of module.key_concepts || []) {
                    allConcepts.push({
                        ...concept,
                        module: module.title,
                        module_id: mid
                    });
                }
            }
        }
        
        return {
            success: true,
            count: allConcepts.length,
            concepts: allConcepts
        };
    },
    
    // 题库API
    async getDeckInfo(deckPath) {
        const deck = DECK_DATA;
        const tags = new Set();
        for (const card of deck.cards) {
            (card.tags || []).forEach(tag => tags.add(tag));
        }
        return {
            success: true,
            title: deck.meta.title,
            source: deck.meta.source,
            total_cards: deck.cards.length,
            tags: Array.from(tags).sort()
        };
    },
    
    async startQuiz(deckPath, n, tags) {
        let pool = DECK_DATA.cards;
        
        if (tags && tags.length > 0) {
            pool = filterCardsByTags(pool, tags);
        }
        
        if (pool.length === 0) {
            return { success: false, error: "没有符合条件的题目" };
        }
        
        n = Math.min(n, pool.length);
        const selected = [];
        const indices = new Set();
        
        while (selected.length < n && indices.size < pool.length) {
            const idx = Math.floor(Math.random() * pool.length);
            if (!indices.has(idx)) {
                indices.add(idx);
                const card = pool[idx];
                const c = {
                    id: card.id,
                    type: card.type,
                    tags: card.tags || []
                };
                if (card.type === 'mcq') {
                    c.stem = card.stem;
                    c.choices = card.choices;
                } else {
                    c.prompt = card.prompt;
                }
                selected.push(c);
            }
        }
        
        return {
            success: true,
            deck_path: deckPath,
            total: selected.length,
            cards: selected
        };
    },
    
    async submitAnswer(deckPath, cardId, answer, elapsedMs) {
        const card = getCardById(cardId);
        if (!card) {
            return { success: false, error: "题目不存在" };
        }
        
        let correct = false;
        if (card.type === 'mcq') {
            if (answer) {
                const idx = letterToIndex(answer);
                if (idx !== null) {
                    correct = gradeMCQ(card, idx);
                }
            }
        } else {
            if (answer) {
                correct = gradeShort(card, answer);
            }
        }
        
        // 更新SRS
        const srs = Storage.getSRS();
        updateSRS(srs, deckPath, cardId, correct);
        Storage.saveSRS(srs);
        
        // 更新错题本
        if (correct) {
            Storage.clearWrongCard(deckPath, cardId);
        } else {
            Storage.addWrongCard(deckPath, cardId);
        }
        
        // 记录
        Storage.logAttempt(deckPath, cardId, card.type, correct, answer || '', elapsedMs);
        
        const result = {
            success: true,
            correct: correct,
            explain: card.explain || ''
        };
        
        if (card.type === 'mcq') {
            result.correct_answer = String.fromCharCode(65 + card.answer_index);
            result.correct_text = card.choices[card.answer_index];
        } else {
            result.correct_answer = card.answer;
        }
        
        // 错题分析
        if (!correct) {
            result.learning_guide = analyzeWrongAnswer(card, answer || '');
        }
        
        return result;
    },
    
    async getReviewCards(deckPath, n, onlyWrong) {
        const srs = Storage.getSRS();
        const dueIds = getDueCardIds(srs, deckPath);
        
        let cards = dueIds.map(id => getCardById(id)).filter(c => c !== null);
        
        if (onlyWrong) {
            const wrong = Storage.getWrongCards(deckPath);
            cards = cards.filter(c => wrong.has(c.id));
        }
        
        n = Math.min(n, cards.length);
        const selected = cards.slice(0, n).map(card => {
            const c = {
                id: card.id,
                type: card.type,
                tags: card.tags || []
            };
            if (card.type === 'mcq') {
                c.stem = card.stem;
                c.choices = card.choices;
            } else {
                c.prompt = card.prompt;
            }
            return c;
        });
        
        return {
            success: true,
            deck_path: deckPath,
            total: selected.length,
            due_total: dueIds.length,
            cards: selected
        };
    },
    
    async getStats(days) {
        const attempts = Storage.getAttempts();
        const now = new Date();
        const cutoff = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
        
        const recent = attempts.filter(a => new Date(a.timestamp) >= cutoff);
        const correct = recent.filter(a => a.correct).length;
        
        const byDay = {};
        recent.forEach(a => {
            const day = a.timestamp.split('T')[0];
            if (!byDay[day]) {
                byDay[day] = { count: 0, correct: 0 };
            }
            byDay[day].count++;
            if (a.correct) byDay[day].correct++;
        });
        
        const byDayList = Object.entries(byDay)
            .map(([day, data]) => ({
                day,
                count: data.count,
                correct: data.correct,
                accuracy: data.count > 0 ? data.correct / data.count : 0
            }))
            .sort((a, b) => a.day.localeCompare(b.day));
        
        return {
            success: true,
            total: attempts.length,
            recent_total: recent.length,
            recent_correct: correct,
            recent_accuracy: recent.length > 0 ? correct / recent.length : 0,
            by_day: byDayList
        };
    },
    
    async getWrongCards(deckPath) {
        const wrong = Storage.getWrongCards(deckPath);
        return {
            success: true,
            deck_path: deckPath,
            wrong_cards: Array.from(wrong).sort(),
            count: wrong.size
        };
    },
    
    async getProgress(deckPath) {
        const deck = DECK_DATA;
        const srs = Storage.getSRS();
        const wrong = Storage.getWrongCards(deckPath);
        const stats = await this.getStats(7);
        
        const moduleProgress = {};
        for (const [moduleId, tags] of Object.entries(MODULE_TAGS)) {
            const moduleCards = deck.cards.filter(c => 
                (c.tags || []).some(t => tags.includes(t))
            );
            
            const deckSRS = srs[deckPath] || {};
            let practiced = 0;
            let mastered = 0;
            
            for (const card of moduleCards) {
                const cardSRS = deckSRS[card.id];
                if (cardSRS) {
                    practiced++;
                    if (cardSRS.interval_days >= 7 && !wrong.has(card.id)) {
                        mastered++;
                    }
                }
            }
            
            moduleProgress[moduleId] = {
                title: KNOWLEDGE_BASE[moduleId].title,
                total: moduleCards.length,
                practiced: practiced,
                mastered: mastered,
                progress: moduleCards.length > 0 ? Math.round(practiced / moduleCards.length * 100) : 0
            };
        }
        
        return {
            success: true,
            total_cards: deck.cards.length,
            wrong_count: wrong.size,
            stats: stats,
            module_progress: moduleProgress
        };
    }
};

// 错题分析
function analyzeWrongAnswer(card, userAnswer) {
    const cardTags = card.tags || [];
    const relatedModules = new Set();
    
    for (const tag of cardTags) {
        const moduleId = getModuleByTag(tag);
        if (moduleId) {
            relatedModules.add(moduleId);
        }
    }
    
    const relatedConcepts = [];
    const relatedConfusions = [];
    const clinicalLinks = [];
    
    for (const moduleId of relatedModules) {
        const module = KNOWLEDGE_BASE[moduleId];
        if (module) {
            relatedConcepts.push(...(module.key_concepts || []).slice(0, 3));
            relatedConfusions.push(...(module.confusions || []));
            clinicalLinks.push(...(module.clinical_links || []).slice(0, 2));
        }
    }
    
    const suggestions = [];
    if (relatedConfusions.length > 0) {
        suggestions.push("注意以下常见混淆点：");
        relatedConfusions.slice(0, 2).forEach(c => {
            suggestions.push(`  • ${c.pair.join(' vs ')}：${c.difference}`);
        });
    }
    
    return {
        analysis: card.explain || '',
        related_concepts: relatedConcepts.slice(0, 3),
        confusions: relatedConfusions.slice(0, 2),
        clinical_links: clinicalLinks.slice(0, 2),
        suggestions: suggestions,
        review_modules: Array.from(relatedModules)
    };
}
