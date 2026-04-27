"""Module 2/4: Statistical metrics - Cohen's kappa, confusion matrix, binary metrics."""


def cohens_kappa(labels1, labels2):
    """Compute Cohen's kappa for two lists of categorical labels."""
    categories = sorted(set(labels1) | set(labels2))
    n = len(labels1)
    if n == 0:
        return 0.0
    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for l1, l2 in zip(labels1, labels2):
        matrix[l1][l2] += 1
    po = sum(matrix[c][c] for c in categories) / n
    pe = sum(
        (sum(matrix[c][c2] for c2 in categories) / n) *
        (sum(matrix[c1][c] for c1 in categories) / n)
        for c in categories
    )
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)


def confusion_matrix_3class(true_labels, pred_labels):
    """3-class confusion matrix: confirmed, suspected, clean."""
    classes = ['confirmed', 'suspected', 'clean']
    return {t: {p: sum(1 for ti, pi in zip(true_labels, pred_labels)
                       if ti == t and pi == p) for p in classes} for t in classes}


def binary_metrics(true_labels, pred_labels):
    """Binary: greenwashing (confirmed+suspected) vs clean."""
    gw = {'confirmed', 'suspected'}
    tp = sum(1 for t, p in zip(true_labels, pred_labels) if t in gw and p in gw)
    tn = sum(1 for t, p in zip(true_labels, pred_labels) if t == 'clean' and p == 'clean')
    fp = sum(1 for t, p in zip(true_labels, pred_labels) if t == 'clean' and p in gw)
    fn = sum(1 for t, p in zip(true_labels, pred_labels) if t in gw and p == 'clean')
    n = len(true_labels)
    acc = (tp + tn) / n if n else 0
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
    fpr = fp / (fp + tn) if (fp + tn) else 0
    return {'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'accuracy': round(acc, 4), 'precision': round(prec, 4),
            'recall': round(rec, 4), 'f1': round(f1, 4), 'fpr': round(fpr, 4)}


def kappa_interpretation(k):
    if k >= 0.81:
        return 'excellent'
    if k >= 0.61:
        return 'substantial'
    if k >= 0.41:
        return 'moderate'
    return 'fair'
