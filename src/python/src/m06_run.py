#!/usr/bin/env python3
"""Main runner: Real RAG vs baseline experiment on GreenClaims corpus."""
import os
import time
from m01_evidence import load_evidence_db, retrieve_evidence, load_corpus
from m02_llm import call_llm, parse_response
from m03_prompts import build_rag_params, build_baseline_params
from m04_metrics import compute_all
from m05_output import build_row, save_results, save_metrics, print_summary

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_ALL = os.path.join(BASE, "data/external/GreenwashingDetectionDataset/GreenClaims.csv")
SRC_35 = os.path.join(BASE, "data/processed/experiment-dataset.csv")
OUT_CSV = os.path.join(BASE, "data/processed/experiment-raw-results.csv")
OUT_JSON = os.path.join(BASE, "data/processed/experiment-metrics.json")


def run_condition(report, evidence_db, use_rag):
    """Run one condition. Returns (label, conf, dur, reason, scores)."""
    try:
        if use_rag:
            evidence = retrieve_evidence(
                report.get("excerpt_summary", ""), report["company"], evidence_db
            )
            r, c, i, f, inp, o, n, e = build_rag_params(report, evidence)
        else:
            r, c, i, f, inp, o, n, e = build_baseline_params(report)
        raw, dur = call_llm(r, c, i, f, inp, o, n, e)
        label, conf, reason, scores = parse_response(raw)
    except Exception as ex:
        label, conf, reason, scores, dur = "suspected", 0.5, str(ex)[:200], {}, 0.0
    return label, conf, dur, reason, scores


def main():
    print("=== Real ESG Greenwashing Detection Experiment ===")
    evidence_db = load_evidence_db(SRC_ALL)
    corpus = load_corpus(SRC_35)
    print(f"Evidence: {len(evidence_db)} | Corpus: {len(corpus)}")

    results, ai_p, man_p, true_l = [], [], [], []
    ai_c, man_c, ai_t, man_t = [], [], [], []

    for i, rpt in enumerate(corpus):
        did, tl = rpt["doc_id"], rpt["label"]
        print(f"  [{i+1}/{len(corpus)}] {did} ({rpt['company']}) true={tl}", end=" ")

        rl, rc, rt, rr, rs = run_condition(rpt, evidence_db, use_rag=True)
        bl, bc, bt, br, bs = run_condition(rpt, evidence_db, use_rag=False)
        print(f"RAG={rl}({rc:.2f},{rt:.1f}s) BASE={bl}({bc:.2f},{bt:.1f}s)")

        true_l.append(tl)
        ai_p.append(rl); man_p.append(bl)
        ai_c.append(rc); man_c.append(bc)
        ai_t.append(rt); man_t.append(bt)

        for cond, lbl, cf, tm, rsn, sc in [
            ("ai_assisted", rl, rc, rt, rr, rs),
            ("manual", bl, bc, bt, br, bs),
        ]:
            results.append(build_row(
                did, rpt["company"], rpt.get("sector", ""), tl,
                cond, lbl, cf, tm, rsn, sc
            ))
        time.sleep(0.3)

    save_results(results, OUT_CSV)
    metrics = compute_all(true_l, ai_p, man_p, ai_c, man_c, ai_t, man_t)
    save_metrics(metrics, OUT_JSON)
    print_summary(metrics)


if __name__ == "__main__":
    main()
