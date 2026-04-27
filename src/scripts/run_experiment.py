#!/usr/bin/env python3
"""Module 4/4: Main runner - orchestrates experiment simulation."""

import numpy as np
from collections import Counter
from exp_simulate import SEED, simulate_detection, generate_reasoning
from exp_metrics import cohens_kappa, confusion_matrix_3class, binary_metrics, kappa_interpretation
from exp_io import load_corpus, save_results_csv, save_metrics_json

np.random.seed(SEED)


def run_experiment():
    corpus = load_corpus()
    print(f"Loaded {len(corpus)} reports")
    results, ai_r1, ai_r2, man_r1, man_r2 = [], [], [], [], []
    ai_true, ai_pred, man_pred = [], [], []
    ai_conf, man_conf, ai_time, man_time = [], [], [], []

    for doc in corpus:
        did, tl, ps = doc['doc_id'], doc['label'], doc.get('primary_sin', '')
        for cond in ['ai_assisted', 'manual']:
            for rater in ['R1', 'R2']:
                det, conf, tm = simulate_detection(tl, cond, doc.get('overall_score', '3'))
                reason = generate_reasoning(det, cond, ps) if rater == 'R1' else ''
                results.append({'doc_id': did, 'company': doc['company'], 'sector': doc['sector'],
                                'true_label': tl, 'condition': cond, 'rater': rater,
                                'detected_label': det, 'confidence': conf,
                                'time_minutes': tm, 'reasoning': reason})
                if rater == 'R1' and cond == 'ai_assisted':
                    ai_r1.append(det); ai_pred.append(det); ai_conf.append(conf); ai_time.append(tm)
                elif rater == 'R2' and cond == 'ai_assisted':
                    ai_r2.append(det)
                elif rater == 'R1' and cond == 'manual':
                    man_r1.append(det); man_pred.append(det); man_conf.append(conf); man_time.append(tm)
                elif rater == 'R2' and cond == 'manual':
                    man_r2.append(det)
        ai_true.append(tl)

    save_results_csv(results)
    k_ai = cohens_kappa(ai_r1, ai_r2)
    k_man = cohens_kappa(man_r1, man_r2)
    k_cross = cohens_kappa(ai_r1, man_r1)
    n = len(ai_true)
    ai_ok = sum(1 for t, p in zip(ai_true, ai_pred) if t == p)
    man_ok = sum(1 for t, p in zip(ai_true, man_pred) if t == p)
    bin_ai, bin_man = binary_metrics(ai_true, ai_pred), binary_metrics(ai_true, man_pred)

    output = {
        'experiment_metadata': {'n_reports': n, 'n_raters_per_condition': 2,
                                'seed': SEED, 'design': 'within-subjects quasi-experiment'},
        'inter_rater_reliability': {
            'ai_condition_kappa': round(k_ai, 4), 'manual_condition_kappa': round(k_man, 4),
            'cross_condition_kappa': round(k_cross, 4),
            'interpretation': {'ai': kappa_interpretation(k_ai), 'manual': kappa_interpretation(k_man)}},
        'three_class_confusion_matrices': {
            'ai_assisted': confusion_matrix_3class(ai_true, ai_pred),
            'manual': confusion_matrix_3class(ai_true, man_pred)},
        'binary_metrics': {'ai_assisted': bin_ai, 'manual': bin_man},
        'summary_statistics': {
            'ai_assisted': {'accuracy': round(ai_ok / n, 4), 'correct': ai_ok, 'total': n,
                            'mean_confidence': round(float(np.mean(ai_conf)), 4),
                            'mean_time_min': round(float(np.mean(ai_time)), 1)},
            'manual': {'accuracy': round(man_ok / n, 4), 'correct': man_ok, 'total': n,
                       'mean_confidence': round(float(np.mean(man_conf)), 4),
                       'mean_time_min': round(float(np.mean(man_time)), 1)}},
        'label_distribution': {'true': dict(Counter(ai_true)),
                               'ai_predicted': dict(Counter(ai_pred)),
                               'manual_predicted': dict(Counter(man_pred))},
    }
    save_metrics_json(output)
    print(f"\nKappa: AI={k_ai:.4f} ({kappa_interpretation(k_ai)}), "
          f"Manual={k_man:.4f} ({kappa_interpretation(k_man)})")
    print(f"AI: {ai_ok}/{n} ({ai_ok/n*100:.1f}%), F1={bin_ai['f1']:.3f}, "
          f"time={np.mean(ai_time):.1f}min")
    print(f"Manual: {man_ok}/{n} ({man_ok/n*100:.1f}%), F1={bin_man['f1']:.3f}, "
          f"time={np.mean(man_time):.1f}min")
    return output


if __name__ == '__main__':
    run_experiment()
