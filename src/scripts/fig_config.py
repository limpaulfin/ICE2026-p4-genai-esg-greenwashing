"""Shared config for publication figures: CUD palette, paths, rcParams."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CUD = {
    'orange': '#E69F00', 'sky_blue': '#56B4E9', 'green': '#009E73',
    'yellow': '#F0E442', 'blue': '#0072B2', 'vermillion': '#D55E00',
    'pink': '#CC79A7',
}

BASE = '/home/fong/Projects/ICE-2026-HUIT/p4-Dung-genai-esg-greenwashing'
FIGDIR = f'{BASE}/python/output'
DATADIR = f'{BASE}/data/processed'

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.labelsize': 11,
    'axes.titlesize': 12, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'legend.fontsize': 9, 'figure.dpi': 300, 'savefig.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})
