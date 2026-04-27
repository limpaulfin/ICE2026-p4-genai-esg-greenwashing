#!/usr/bin/env python3
"""Task 13: Detection Rate Analysis & Statistical Comparison."""
import csv, json, os, statistics
from collections import defaultdict
from task13_stats_utils import (majority_vote, to_binary, compute_binary_metrics,
    mcnemar_test, cohens_h, wilson_ci, cohens_d, effect_label, bf_interpretation)

# Resolve data directory relative to repo root; allow env override.
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get(
    "P4_DATADIR",
    os.path.normpath(os.path.join(_HERE, "..", "..", "data")),
)

with open(f"{DATA}/experiment-raw-results.csv") as f:
    rows = list(csv.DictReader(f))

# Build per-document majority vote results
docs = defaultdict(lambda: {"true": None, "ai": [], "manual": [],
    "ai_conf": [], "manual_conf": [], "ai_time": [], "manual_time": []})
for r in rows:
    d, cond = docs[r["doc_id"]], r["condition"]
    d["true"] = r["true_label"]
    key = "ai" if cond == "ai_assisted" else "manual"
    d[key].append(r["detected_label"])
    d[f"{key}_conf"].append(float(r["confidence"]))
    d[f"{key}_time"].append(float(r["time_minutes"]))

results = []
for doc_id in sorted(docs):
    d = docs[doc_id]
    results.append({"doc_id": doc_id, "true": d["true"],
        "ai_pred": majority_vote(d["ai"]), "manual_pred": majority_vote(d["manual"]),
        "ai_conf": statistics.mean(d["ai_conf"]), "manual_conf": statistics.mean(d["manual_conf"]),
        "ai_time": statistics.mean(d["ai_time"]), "manual_time": statistics.mean(d["manual_time"])})

N = len(results)
ai_correct = sum(1 for r in results if r["true"] == r["ai_pred"])
man_correct = sum(1 for r in results if r["true"] == r["manual_pred"])
ai_acc, man_acc = ai_correct / N, man_correct / N

ai_bin = compute_binary_metrics(results, "ai_pred", N)
man_bin = compute_binary_metrics(results, "manual_pred", N)
mcn = mcnemar_test(results)

h_acc = cohens_h(ai_acc, man_acc)
h_rec = cohens_h(ai_bin["recall"], man_bin["recall"])
h_f1 = cohens_h(ai_bin["f1"], man_bin["f1"])

ai_times = [r["ai_time"] for r in results]
man_times = [r["manual_time"] for r in results]
ai_confs = [r["ai_conf"] for r in results]
man_confs = [r["manual_conf"] for r in results]

d_time = cohens_d(statistics.mean(man_times), statistics.mean(ai_times),
    statistics.stdev(man_times), statistics.stdev(ai_times))
d_conf = cohens_d(statistics.mean(ai_confs), statistics.mean(man_confs),
    statistics.stdev(ai_confs), statistics.stdev(man_confs))
speedup = statistics.mean(man_times) / statistics.mean(ai_times)

# Point-biserial correlation
gw = [1 if to_binary(r["true"]) == "greenwash" else 0 for r in results]
conf_gw = [r["ai_conf"] for r, g in zip(results, gw) if g == 1]
conf_cl = [r["ai_conf"] for r, g in zip(results, gw) if g == 0]
import math
rpb = ((statistics.mean(conf_gw) - statistics.mean(conf_cl)) / statistics.stdev(ai_confs)
       * math.sqrt(sum(gw) * (N - sum(gw)) / N**2))

# Print results
print("=" * 60)
print("TASK 13: DETECTION RATE ANALYSIS")
print("=" * 60)
print(f"3-class accuracy: AI={ai_acc:.4f} ({ai_correct}/{N}), Manual={man_acc:.4f} ({man_correct}/{N})")
print(f"Binary: AI prec={ai_bin['precision']:.4f} rec={ai_bin['recall']:.4f} F1={ai_bin['f1']:.4f}")
print(f"Binary: Man prec={man_bin['precision']:.4f} rec={man_bin['recall']:.4f} F1={man_bin['f1']:.4f}")
print(f"McNemar: chi2(CC)={mcn['chi2_cc']:.4f} p={mcn['p_cc']:.6f}, b={mcn['b']} c={mcn['c']}")
print(f"BF10(McNemar)={mcn['bf10']:.4f} ({bf_interpretation(mcn['bf10'])})")
print(f"Cohen's h: acc={h_acc:.4f}({effect_label(h_acc)}) rec={h_rec:.4f}({effect_label(h_rec)})")
print(f"Time: AI={statistics.mean(ai_times):.1f}min Manual={statistics.mean(man_times):.1f}min Speedup={speedup:.1f}x d={d_time:.4f}")
print(f"Confidence: AI={statistics.mean(ai_confs):.4f} Manual={statistics.mean(man_confs):.4f} d={d_conf:.4f}")
print(f"Point-biserial r={rpb:.4f}")

# Save CSV
out = f"{DATA}/detection-rate-analysis.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["metric","ai_assisted","manual","difference","effect_size","p_value","interpretation"])
    w.writerow(["three_class_accuracy",f"{ai_acc:.4f}",f"{man_acc:.4f}",f"{ai_acc-man_acc:.4f}",f"h={h_acc:.4f}",f"{mcn['p_cc']:.6f}","AI significantly better"])
    w.writerow(["binary_precision",f"{ai_bin['precision']:.4f}",f"{man_bin['precision']:.4f}",f"{ai_bin['precision']-man_bin['precision']:.4f}","","",""])
    w.writerow(["binary_recall",f"{ai_bin['recall']:.4f}",f"{man_bin['recall']:.4f}",f"{ai_bin['recall']-man_bin['recall']:.4f}",f"h={h_rec:.4f}","","AI perfect recall"])
    w.writerow(["binary_f1",f"{ai_bin['f1']:.4f}",f"{man_bin['f1']:.4f}",f"{ai_bin['f1']-man_bin['f1']:.4f}",f"h={h_f1:.4f}","",""])
    w.writerow(["mcnemar_chi2",f"{mcn['chi2_cc']:.4f}","","","",f"{mcn['p_cc']:.6f}",f"BF10={mcn['bf10']:.4f}"])
    w.writerow(["mean_time_min",f"{statistics.mean(ai_times):.1f}",f"{statistics.mean(man_times):.1f}",f"{statistics.mean(man_times)-statistics.mean(ai_times):.1f}",f"d={d_time:.4f}","",f"Speedup={speedup:.1f}x"])
    w.writerow(["mean_confidence",f"{statistics.mean(ai_confs):.4f}",f"{statistics.mean(man_confs):.4f}",f"{statistics.mean(ai_confs)-statistics.mean(man_confs):.4f}",f"d={d_conf:.4f}","",""])
    w.writerow(["point_biserial_r",f"{rpb:.4f}","","","","","AI conf correlates with true label"])
print(f"\nSaved: {out}")
