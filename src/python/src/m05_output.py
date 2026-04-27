"""Save experiment results and print summary."""
import csv
import json


def build_row(doc_id, company, sector, true_label, cond, lbl, cf, tm, rsn, sc):
    """Build one result row dict."""
    return {
        "doc_id": doc_id, "company": company, "sector": sector,
        "true_label": true_label, "condition": cond,
        "detected_label": lbl, "confidence": cf,
        "time_seconds": round(tm, 2), "reasoning": rsn,
        "vagueness": sc.get("vagueness", ""),
        "selectivity": sc.get("selectivity", ""),
        "misleading": sc.get("misleading", ""),
        "irrelevance": sc.get("irrelevance", ""),
        "overall_risk": sc.get("overall_risk", ""),
    }


def save_results(results, out_csv):
    """Save results list to CSV."""
    if not results:
        return
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"Saved: {out_csv}")


def save_metrics(metrics, out_json):
    """Save metrics dict to JSON."""
    with open(out_json, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Saved: {out_json}")


def print_summary(m):
    """Print experiment summary."""
    sep = "=" * 55
    print(f"\n{sep}")
    print(f"3-class: AI={m['ai_accuracy']*100:.1f}% "
          f"Manual={m['man_accuracy']*100:.1f}%")
    ab, mb = m["ai_binary"], m["man_binary"]
    print(f"F1: AI={ab['f1']:.3f} Manual={mb['f1']:.3f}")
    print(f"Recall: AI={ab['recall']:.3f} Manual={mb['recall']:.3f}")
    h = m["cohens_h"]
    print(f"Cohen's h: acc={h['accuracy']:.3f} rec={h['recall']:.3f} "
          f"f1={h['f1']:.3f}")
    mc = m["mcnemar"]
    print(f"McNemar: b={mc['b']} c={mc['c']} chi2={mc['chi2_cc']:.3f}")
    c = m["confidence"]
    print(f"Confidence: AI={c['ai']:.3f} Manual={c['manual']:.3f}")
    print(sep)
