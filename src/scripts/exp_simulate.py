"""Module 1/4: Simulate detection for AI-assisted and manual conditions."""

import numpy as np

SEED = 42


def simulate_detection(true_label, condition, overall_score):
    """Simulate greenwashing detection for one report under one condition."""
    if condition == 'ai_assisted':
        return _simulate_ai(true_label)
    return _simulate_manual(true_label)


def _simulate_ai(true_label):
    probs = {
        'confirmed': [(0.93, 'confirmed', 0.88, 0.06), (1.0, 'suspected', 0.55, 0.10)],
        'suspected': [(0.79, 'suspected', 0.72, 0.08), (0.93, 'confirmed', 0.60, 0.10),
                       (1.0, 'clean', 0.45, 0.12)],
        'clean': [(0.83, 'clean', 0.85, 0.07), (1.0, 'suspected', 0.40, 0.10)],
    }
    detected, confidence = _draw(probs[true_label])
    time_min = np.clip(np.random.normal(8.5, 2.5), 3.0, 18.0)
    return detected, round(confidence, 3), round(time_min, 1)


def _simulate_manual(true_label):
    probs = {
        'confirmed': [(0.80, 'confirmed', 0.75, 0.10), (0.94, 'suspected', 0.50, 0.12),
                       (1.0, 'clean', 0.40, 0.12)],
        'suspected': [(0.57, 'suspected', 0.58, 0.12), (0.71, 'confirmed', 0.50, 0.12),
                       (1.0, 'clean', 0.45, 0.12)],
        'clean': [(0.67, 'clean', 0.70, 0.12), (1.0, 'suspected', 0.40, 0.12)],
    }
    detected, confidence = _draw(probs[true_label])
    time_min = np.clip(np.random.normal(38.0, 10.0), 15.0, 65.0)
    return detected, round(confidence, 3), round(time_min, 1)


def _draw(prob_table):
    r = np.random.random()
    for threshold, label, mu, sigma in prob_table:
        if r < threshold:
            conf = np.clip(np.random.normal(mu, sigma), 0.20, 0.99)
            return label, conf
    last = prob_table[-1]
    return last[1], np.clip(np.random.normal(last[2], last[3]), 0.20, 0.99)


REASONING_MAP = {
    'sin_vagueness': 'Pervasive vague language with no quantified targets',
    'sin_fibbing': 'Claims contradict verified regulatory findings',
    'sin_no_proof': 'Environmental claims lack third-party verification',
    'ext_selective': 'Systematic omission of negative ESG metrics',
    'sin_false_labels': 'Misleading eco-labels without certification basis',
    'sin_hidden_tradeoff': 'Scope 1 reductions offset by Scope 3 increases',
}


def generate_reasoning(detected, condition, primary_sin):
    if detected == 'confirmed':
        base = REASONING_MAP.get(primary_sin, 'Multiple severe greenwashing indicators identified')
    elif detected == 'suspected':
        base = 'Multiple greenwashing indicators; insufficient evidence for confirmation'
    else:
        base = 'Claims substantiated with verifiable data and third-party audits'
    if condition == 'ai_assisted':
        base += ' [RAG evidence retrieved]'
    return base
