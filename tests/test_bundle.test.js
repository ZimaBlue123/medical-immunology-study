const test = require('node:test');
const assert = require('node:assert/strict');
const ImmunoStudy = require('../index.js');

test('ImmunoStudy initialization', () => {
  assert.equal(ImmunoStudy.version, '1.0.0');
  assert.equal(Array.isArray(ImmunoStudy.MODULES), true);
  assert.equal(ImmunoStudy.MODULES.length, 12);
  assert.equal(ImmunoStudy.MODULES[0].id, 'module01');
});

test('Engine text normalization', () => {
  const { normalizeText } = ImmunoStudy.engine;
  assert.equal(normalizeText('  T  Cells '), 't cells');
  assert.equal(normalizeText('Innate\t\nImmunity'), 'innate immunity');
});

test('Engine letter to index conversion', () => {
  const { letterToIndex, indexToLetter } = ImmunoStudy.engine;
  assert.equal(letterToIndex('A'), 0);
  assert.equal(letterToIndex('b'), 1);
  assert.equal(letterToIndex('D'), 3);
  assert.equal(letterToIndex('invalid'), null);
  assert.equal(indexToLetter(0), 'A');
  assert.equal(indexToLetter(2), 'C');
});

test('Engine MCQ and short answer grading', () => {
  const { gradeMcq, gradeShort } = ImmunoStudy.engine;
  const mcqCard = { id: 'q1', answer_index: 2 };
  assert.equal(gradeMcq(mcqCard, 2), true);
  assert.equal(gradeMcq(mcqCard, 0), false);

  const shortCard = { id: 'q2', answer: 'Interferon-gamma' };
  assert.equal(gradeShort(shortCard, 'interferon-gamma'), true);
  assert.equal(gradeShort(shortCard, '  INTERFERON-GAMMA  '), true);
  assert.equal(gradeShort(shortCard, 'IL-4'), false);
});

test('SRS state progression and decay', () => {
  const { defaultSrsState, updateSrsState, isDue } = ImmunoStudy.srs;
  const base = defaultSrsState('card_test');
  assert.equal(base.consecutive_correct, 0);

  // First correct answer
  const step1 = updateSrsState(base, true, new Date('2026-09-01'));
  assert.equal(step1.consecutive_correct, 1);
  assert.equal(step1.interval_days, 1);
  assert.equal(step1.due_date, '2026-09-02');

  // Second correct answer
  const step2 = updateSrsState(step1, true, new Date('2026-09-02'));
  assert.equal(step2.consecutive_correct, 2);
  assert.equal(step2.interval_days, 6);
  assert.equal(step2.due_date, '2026-09-08');

  // Third correct answer (interval * easeFactor)
  const step3 = updateSrsState(step2, true, new Date('2026-09-08'));
  assert.equal(step3.consecutive_correct, 3);
  assert.equal(step3.interval_days, 15);

  // Failure resets streak and drops ease factor
  const failed = updateSrsState(step3, false, new Date('2026-09-23'));
  assert.equal(failed.consecutive_correct, 0);
  assert.equal(failed.interval_days, 1);
  assert.equal(failed.ease_factor, 2.3);

  // Due check
  assert.equal(isDue(step1, new Date('2026-09-05')), true);
  assert.equal(isDue(step2, new Date('2026-09-03')), false);
});
