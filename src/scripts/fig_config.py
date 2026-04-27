"""Shared config for publication figures: CUD palette, paths, rcParams."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CUD = {
    'orange': '#E69F00', 'sky_blue': '#56B4E9', 'green': '#009E73',
    'yellow': '#F0E442', 'blue': '#0072B2', 'vermillion': '#D55E00',
    'pink': '#CC79A7',
}

# Resolve repository root from this file location; allow env override.
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get('P4_BASE', os.path.normpath(os.path.join(HERE, '..', '..')))
FIGDIR = os.environ.get('P4_FIGDIR', os.path.join(BASE, 'output'))
DATADIR = os.environ.get('P4_DATADIR', os.path.join(BASE, 'data'))

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.labelsize': 11,
    'axes.titlesize': 12, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'legend.fontsize': 9, 'figure.dpi': 300, 'savefig.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})
