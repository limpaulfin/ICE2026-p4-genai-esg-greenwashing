"""Statistics computation for real experiment results."""
import math


def cohens_h(p1, p2):
    """Cohen's h effect size for two proportions."""
    return abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))


def binary_stats(true_bin, pred_bin, pos="gw"):
    """Binary classification metrics."""
    tp = sum(1 for t, p in zip(true_bin, pred_bin) if t == pos and p == pos)
    fp = sum(1 for t, p in zip(true_bin, pred_bin) if t != pos and p == pos)
    fn = sum(1 for t, p in zip(true_bin, pred_bin) if t == pos and p != pos)
    tn = sum(1 for t, p in zip(true_bin, pred_bin) if t != pos and p != pos)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(f1, 4)}


def to_binary(labels):
    """Convert 3-class to binary (greenwashing vs clean)."""
    return ["gw" if l in ("confirmed", "suspected") else "clean" for l in labels]


def confusion_matrix_3class(true_l, pred_l):
    """3-class confusion matrix."""
    order = ["confirmed", "suspected", "clean"]
    cm = {t: {p: 0 for p in order} for t in order}
    for t, p in zip(true_l, pred_l):
        if t in cm and p in cm[t]:
            cm[t][p] += 1
    return cm


def mcnemar_test(ai_correct, man_correct):
    """McNemar test with continuity correction."""
    b = sum(1 for a, m in zip(ai_correct, man_correct) if a and not m)
    c = sum(1 for a, m in zip(ai_correct, man_correct) if not a and m)
    chi2 = ((abs(b - c) - 1) ** 2) / (b + c) if (b + c) > 0 else 0
    return b, c, round(chi2, 4)


def compute_all(true_labels, ai_preds, man_preds,
                ai_confs, man_confs, ai_times, man_times):
    """Compute all experiment metrics. Returns dict."""
    import numpy as np
    n = len(true_labels)
    ai_ok = sum(1 for t, p in zip(true_labels, ai_preds) if t == p)
    man_ok = sum(1 for t, p in zip(true_labels, man_preds) if t == p)

    true_bin, ai_bin, man_bin = to_binary(true_labels), to_binary(ai_preds), to_binary(man_preds)
    ai_binary = binary_stats(true_bin, ai_bin)
    man_binary = binary_stats(true_bin, man_bin)

    ai_correct = [t == p for t, p in zip(true_labels, ai_preds)]
    man_correct = [t == p for t, p in zip(true_labels, man_preds)]
    b, c, chi2 = mcnemar_test(ai_correct, man_correct)

    h_acc = cohens_h(ai_ok / n, man_ok / n) if n > 0 else 0
    h_rec = cohens_h(ai_binary["recall"], man_binary["recall"])
    h_f1 = cohens_h(ai_binary["f1"], man_binary["f1"])

    from collections import Counter
    return {
        "n": n,
        "ai_accuracy": round(ai_ok / n, 4), "man_accuracy": round(man_ok / n, 4),
        "ai_correct": ai_ok, "man_correct": man_ok,
        "ai_binary": ai_binary, "man_binary": man_binary,
        "confusion_ai": confusion_matrix_3class(true_labels, ai_preds),
        "confusion_man": confusion_matrix_3class(true_labels, man_preds),
        "mcnemar": {"b": b, "c": c, "chi2_cc": chi2},
        "cohens_h": {"accuracy": round(h_acc, 4), "recall": round(h_rec, 4), "f1": round(h_f1, 4)},
        "confidence": {"ai": round(float(np.mean(ai_confs)), 4),
                       "manual": round(float(np.mean(man_confs)), 4)},
        "timing": {"ai_mean": round(float(np.mean(ai_times)), 2),
                   "manual_mean": round(float(np.mean(man_times)), 2)},
        "dist_true": dict(Counter(true_labels)),
        "dist_ai": dict(Counter(ai_preds)),
        "dist_man": dict(Counter(man_preds)),
    }
