#!/usr/bin/env python3
"""Entry point: Real ESG Greenwashing Detection Experiment.
Usage: /home/fong/Projects/.venv/bin/python main.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from m06_run import main

if __name__ == "__main__":
    main()
