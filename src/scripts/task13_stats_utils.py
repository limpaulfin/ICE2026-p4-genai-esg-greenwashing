"""Statistical utility functions for detection rate analysis."""
import math
import statistics
from collections import defaultdict

severity = {"confirmed": 3, "suspected": 2, "clean": 1}

def majority_vote(labels):
    counts = defaultdict(int)
    for l in labels:
        counts[l] += 1
    max_count = max(counts.values())
    candidates = [l for l, c in counts.items() if c == max_count]
    return max(candidates, key=lambda x: severity.get(x, 0))

def to_binary(label):
    return "greenwash" if label in ("confirmed", "suspected") else "clean"

def compute_binary_metrics(results, pred_key, N):
    tp = fp = tn = fn = 0
    for r in results:
        t, p = to_binary(r["true"]), to_binary(r[pred_key])
        if t == "greenwash" and p == "greenwash": tp += 1
        elif t == "greenwash" and p == "clean": fn += 1
        elif t == "clean" and p == "greenwash": fp += 1
        else: tn += 1
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "precision": prec, "recall": rec, "f1": f1, "accuracy": (tp + tn) / N}

def mcnemar_test(results):
    a = b = c = d = 0
    for r in results:
        ai_ok = r["true"] == r["ai_pred"]
        man_ok = r["true"] == r["manual_pred"]
        if ai_ok and man_ok: a += 1
        elif ai_ok and not man_ok: b += 1
        elif not ai_ok and man_ok: c += 1
        else: d += 1
    disc = b + c
    chi2_cc = (abs(b - c) - 1) ** 2 / disc if disc else 0
    chi2 = (b - c) ** 2 / disc if disc else 0
    p_cc = 2 * (1 - norm_cdf(math.sqrt(chi2_cc)))
    p_no = 2 * (1 - norm_cdf(math.sqrt(chi2)))
    bf10 = compute_bf10_mcnemar(b, c, disc)
    return {"a": a, "b": b, "c": c, "d": d, "chi2_cc": chi2_cc,
            "chi2": chi2, "p_cc": p_cc, "p_no_cc": p_no, "bf10": bf10}

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def compute_bf10_mcnemar(b, c, disc):
    if disc == 0: return 1.0
    from math import lgamma, log
    log_h0 = lgamma(disc + 1) - lgamma(b + 1) - lgamma(c + 1) + disc * log(0.5)
    log_h1 = -log(disc + 1)
    return math.exp(log_h1 - log_h0)

def cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))

def wilson_ci(p, n, z=1.96):
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0, center - spread), min(1, center + spread))

def cohens_d(m1, m2, sd1, sd2):
    pooled = math.sqrt((sd1**2 + sd2**2) / 2)
    return (m1 - m2) / pooled if pooled else 0

def effect_label(val, thresholds=(0.2, 0.5, 0.8)):
    v = abs(val)
    if v >= thresholds[2]: return "large"
    elif v >= thresholds[1]: return "medium"
    return "small"

def bf_interpretation(bf):
    if bf > 100: return "extreme"
    elif bf > 30: return "very strong"
    elif bf > 10: return "strong"
    elif bf > 3: return "moderate"
    elif bf > 1: return "anecdotal"
    return "against H1"
