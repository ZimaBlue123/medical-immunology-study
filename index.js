/**
 * Medical Immunology Study System - Frontend JavaScript Engine
 * Provides client-side grading, SRS calculations, and module metadata.
 */

'use strict';

const MODULES = [
  { id: 'module01', title: '免疫学总论与基本概念', enTitle: 'Overview and Basic Concepts', tag: 'module01' },
  { id: 'module02', title: '固有免疫系统', enTitle: 'Innate Immune System', tag: 'module02' },
  { id: 'module03', title: '补体系统', enTitle: 'Complement System', tag: 'module03' },
  { id: 'module04', title: '抗原与MHC分子', enTitle: 'Antigens and MHC Molecules', tag: 'module04' },
  { id: 'module05', title: '免疫球蛋白与抗体', enTitle: 'Immunoglobulins and Antibodies', tag: 'module05' },
  { id: 'module06', title: 'T细胞与细胞免疫', enTitle: 'T Cells and Cellular Immunity', tag: 'module06' },
  { id: 'module07', title: 'B细胞与体液免疫', enTitle: 'B Cells and Humoral Immunity', tag: 'module07' },
  { id: 'module08', title: '细胞因子与趋化因子', enTitle: 'Cytokines and Chemokines', tag: 'module08' },
  { id: 'module09', title: '超敏反应', enTitle: 'Hypersensitivity Reactions', tag: 'module09' },
  { id: 'module10', title: '自身免疫与免疫耐受', enTitle: 'Autoimmunity and Immune Tolerance', tag: 'module10' },
  { id: 'module11', title: '免疫缺陷病', enTitle: 'Immunodeficiency Diseases', tag: 'module11' },
  { id: 'module12', title: '肿瘤免疫与移植免疫', enTitle: 'Tumor and Transplantation Immunology', tag: 'module12' },
];

function normalizeText(text) {
  if (typeof text !== 'string') return '';
  return text.trim().toLowerCase().replace(/\s+/g, ' ');
}

function letterToIndex(letter) {
  if (!letter || typeof letter !== 'string') return null;
  const s = letter.trim().toUpperCase();
  if (s.length === 1 && s >= 'A' && s <= 'Z') {
    return s.charCodeAt(0) - 65;
  }
  return null;
}

function indexToLetter(index) {
  if (typeof index !== 'number' || index < 0 || index > 25) return '';
  return String.fromCharCode(65 + index);
}

function gradeMcq(card, userIndex) {
  if (!card || card.answer_index === undefined || userIndex === null || userIndex === undefined) {
    return false;
  }
  return Number(userIndex) === Number(card.answer_index);
}

function gradeShort(card, userText) {
  if (!card || typeof card.answer !== 'string') {
    return false;
  }
  return normalizeText(userText) === normalizeText(card.answer);
}

function defaultSrsState(cardId) {
  return {
    card_id: cardId,
    interval_days: 1,
    ease_factor: 2.5,
    due_date: new Date().toISOString().split('T')[0],
    consecutive_correct: 0,
    total_reviews: 0,
  };
}

function updateSrsState(state, isCorrect, reviewDate = new Date()) {
  const s = { ...(state || defaultSrsState('unknown')) };
  s.total_reviews = (s.total_reviews || 0) + 1;

  if (isCorrect) {
    s.consecutive_correct = (s.consecutive_correct || 0) + 1;
    if (s.consecutive_correct === 1) {
      s.interval_days = 1;
    } else if (s.consecutive_correct === 2) {
      s.interval_days = 6;
    } else {
      s.interval_days = Math.max(1, Math.round(s.interval_days * (s.ease_factor || 2.5)));
    }
  } else {
    s.consecutive_correct = 0;
    s.interval_days = 1;
    s.ease_factor = Math.max(1.3, (s.ease_factor || 2.5) - 0.2);
  }

  const nextDue = new Date(reviewDate);
  nextDue.setDate(nextDue.getDate() + s.interval_days);
  s.due_date = nextDue.toISOString().split('T')[0];

  return s;
}

function isDue(state, currentDate = new Date()) {
  if (!state || !state.due_date) return true;
  const todayStr = (currentDate instanceof Date ? currentDate : new Date(currentDate))
    .toISOString()
    .split('T')[0];
  return state.due_date <= todayStr;
}

const ImmunoStudy = {
  version: '1.0.0',
  MODULES,
  engine: {
    normalizeText,
    letterToIndex,
    indexToLetter,
    gradeMcq,
    gradeShort,
  },
  srs: {
    defaultSrsState,
    updateSrsState,
    isDue,
  },
};

module.exports = ImmunoStudy;
module.exports.default = ImmunoStudy;
