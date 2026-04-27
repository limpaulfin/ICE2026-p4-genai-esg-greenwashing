#!/usr/bin/env python3
"""Figure 3: Detection comparison + Figure 4: Confusion heatmaps.
Reads from experiment-metrics.json (SSoT)."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json, os
from fig_config import CUD, FIGDIR, DATADIR


def load_metrics():
    with open(os.path.join(DATADIR, 'experiment-metrics.json')) as f:
        return json.load(f)


def fig3_detection_comparison(m):
    metrics = ['Three-class\nAccuracy', 'Precision', 'Recall', 'F1-Score']
    ai = [m['ai_accuracy'], m['ai_binary']['precision'],
          m['ai_binary']['recall'], m['ai_binary']['f1']]
    man = [m['man_accuracy'], m['man_binary']['precision'],
           m['man_binary']['recall'], m['man_binary']['f1']]
    x, w = np.arange(len(metrics)), 0.32

    fig, ax = plt.subplots(figsize=(6.5, 4))
    b1 = ax.bar(x - w/2, ai, w, label='RAG-Augmented',
                color=CUD['blue'], edgecolor='white', lw=0.5)
    b2 = ax.bar(x + w/2, man, w, label='Baseline LLM',
                color=CUD['vermillion'], edgecolor='white', lw=0.5)
    for bars, bold in [(b1, True), (b2, False)]:
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, h + 0.01, f'{h:.3f}',
                    ha='center', va='bottom', fontsize=8,
                    fontweight='bold' if bold else 'normal')
    ax.set_ylabel('Score')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylim(0, 1.12)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
    ax.legend(loc='upper left', framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, ls='--')
    fig.savefig(os.path.join(FIGDIR, 'detection-comparison.png'))
    plt.close(fig)
    print('Saved: detection-comparison.png')


def fig4_confusion_heatmaps(m):
    labels = ['Confirmed', 'Suspected', 'Clean']
    keys = ['confirmed', 'suspected', 'clean']

    def to_mat(cm):
        return np.array([[cm[t][p] for p in keys] for t in keys])

    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2))
    for ax, cm_data, title, cmap in [
        (axes[0], m['confusion_ai'], 'RAG-Augmented', 'Blues'),
        (axes[1], m['confusion_man'], 'Baseline LLM', 'Oranges'),
    ]:
        cm = to_mat(cm_data)
        ax.imshow(cm, cmap=cmap, vmin=0, vmax=15)
        ax.set_title(title, fontweight='bold', pad=8)
        ax.set_xticks(range(3)); ax.set_yticks(range(3))
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel('Predicted'); ax.set_ylabel('True Label')
        for i in range(3):
            for j in range(3):
                v = int(cm[i, j])
                ax.text(j, i, str(v), ha='center', va='center',
                        fontsize=12, fontweight='bold',
                        color='white' if v > 8 else 'black')
    fig.tight_layout(w_pad=2)
    fig.savefig(os.path.join(FIGDIR, 'confusion-heatmaps.png'))
    plt.close(fig)
    print('Saved: confusion-heatmaps.png')


if __name__ == '__main__':
    m = load_metrics()
    fig3_detection_comparison(m)
    fig4_confusion_heatmaps(m)
