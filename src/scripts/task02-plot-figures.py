#!/usr/bin/env python3
"""Task 02: Generate GHG comparison and renewable trend figures."""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, 'data', 'processed')
FIGURES = os.path.join(BASE, 'python', 'output')

CUD = {
    'Korea, Rep.': ('#E69F00', '-', 2.5),
    'United States': ('#56B4E9', '--', 1.5),
    'Japan': ('#009E73', '--', 1.5),
    'Germany': ('#F0E442', '--', 1.5),
    'France': ('#0072B2', '--', 1.5),
}

def plot_ghg_comparison():
    ghg = pd.read_csv(os.path.join(PROCESSED, 'multi-country-ghg-comparison.csv'), index_col=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    for country in ghg.columns:
        color, ls, lw = CUD.get(country, ('#CC79A7', '--', 1.5))
        ax.plot(ghg.index, ghg[country], label=country, color=color,
                linewidth=lw, linestyle=ls, marker='o', markersize=4)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('CO$_2$ Emissions (Mt CO$_2$e)', fontsize=12)
    ax.set_title('GHG Emissions: Korea vs Selected Economies (2010-2022)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(ghg.index)
    ax.set_xticklabels(ghg.index.astype(int), rotation=45)
    plt.tight_layout()
    path = os.path.join(FIGURES, 'ghg-comparison.png')
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

def plot_renewable_trend():
    ind = pd.read_csv(os.path.join(PROCESSED, 'korea-esg-indicators.csv'))
    ren = ind.dropna(subset=['renewable_pct'])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(ren['year'], ren['renewable_pct'], color='#009E73', alpha=0.7,
           edgecolor='#006B4F', linewidth=0.8)
    ax.plot(ren['year'], ren['renewable_pct'], color='#E69F00',
            linewidth=2, marker='o', markersize=6, zorder=5)
    for row in [ren.iloc[0], ren.iloc[-1]]:
        ax.annotate(f"{row['renewable_pct']:.1f}%", (row['year'], row['renewable_pct']),
                    textcoords="offset points", xytext=(0, 12),
                    ha='center', fontsize=10, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Renewable Energy Share (%)', fontsize=12)
    ax.set_title('Korea: Renewable Energy Consumption (2010-2022)',
                 fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticks(ren['year'])
    ax.set_xticklabels(ren['year'].astype(int), rotation=45)
    ax.set_ylim(0, ren['renewable_pct'].max() * 1.3)
    plt.tight_layout()
    path = os.path.join(FIGURES, 'renewable-trend.png')
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

if __name__ == '__main__':
    plot_ghg_comparison()
    plot_renewable_trend()
