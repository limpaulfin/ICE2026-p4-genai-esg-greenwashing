#!/usr/bin/env python3
"""Figure 5: Time-to-audit boxplot + Figure 7: Framework radar.
Reads from experiment-raw-results.csv and experiment-metrics.json (SSoT)."""
import matplotlib.pyplot as plt
import numpy as np
import csv, json, os
from fig_config import CUD, FIGDIR, DATADIR


def fig5_time_boxplot():
    ai_t, man_t = [], []
    with open(os.path.join(DATADIR, 'experiment-raw-results.csv')) as f:
        for row in csv.DictReader(f):
            t = float(row['time_seconds'])
            (ai_t if row['condition'] == 'ai_assisted' else man_t).append(t)

    fig, ax = plt.subplots(figsize=(5, 4))
    bp = ax.boxplot([ai_t, man_t], labels=['RAG-Augmented', 'Baseline LLM'],
                    patch_artist=True, widths=0.5,
                    medianprops=dict(color='black', lw=1.5),
                    whiskerprops=dict(lw=1), capprops=dict(lw=1))
    bp['boxes'][0].set(facecolor=CUD['blue'], alpha=0.7)
    bp['boxes'][1].set(facecolor=CUD['vermillion'], alpha=0.7)

    ai_m, man_m = np.mean(ai_t), np.mean(man_t)
    ax.scatter([1, 2], [ai_m, man_m], marker='D', color=CUD['green'],
               s=50, zorder=5,
               label=f'Mean (RAG={ai_m:.1f}s, Base={man_m:.1f}s)')
    ax.set_ylabel('API Response Time (seconds)')
    ax.set_ylim(0, max(max(ai_t), max(man_t)) * 1.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, ls='--')
    ax.legend(loc='upper left', fontsize=8)
    fig.savefig(os.path.join(FIGDIR, 'time-audit-boxplot.png'))
    plt.close(fig)
    print('Saved: time-audit-boxplot.png')


def fig7_framework_radar():
    with open(os.path.join(DATADIR, 'experiment-metrics.json')) as f:
        m = json.load(f)
    cats = ['Data Integrity\n(Binary Recall)',
            'Transparency\n(Evidence Cited)',
            'Provenance\n(Suspected Det.)',
            'Human Oversight\n(FP Correctability)']
    ai = [m['ai_binary']['recall'], 1.0,
          m['confusion_ai']['suspected']['suspected'] / 14, 1.0]
    man = [m['man_binary']['recall'], 0.0,
           m['confusion_man']['suspected']['suspected'] / 14, 1.0]
    N = len(cats)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ai_c = ai + [ai[0]]
    man_c = man + [man[0]]
    ang_c = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(ang_c, ai_c, 'o-', color=CUD['blue'], lw=2,
            label='RAG-Augmented', ms=6)
    ax.fill(ang_c, ai_c, color=CUD['blue'], alpha=0.15)
    ax.plot(ang_c, man_c, 's--', color=CUD['vermillion'], lw=2,
            label='Baseline LLM', ms=6)
    ax.fill(ang_c, man_c, color=CUD['vermillion'], alpha=0.1)
    ax.set_xticks(angles)
    ax.set_xticklabels(cats, fontsize=8)
    ax.tick_params(axis='x', pad=15)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'],
                       fontsize=7, color='gray')
    ax.legend(loc='lower right', bbox_to_anchor=(1.15, -0.05), fontsize=9)
    fig.savefig(os.path.join(FIGDIR, 'framework-radar.png'))
    plt.close(fig)
    print('Saved: framework-radar.png')


if __name__ == '__main__':
    fig5_time_boxplot()
    fig7_framework_radar()
