"""Module 3/4: I/O - load corpus, save CSV, save JSON."""

import csv
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
INPUT_CSV = os.path.join(DATA_DIR, 'experiment-dataset.csv')
OUTPUT_CSV = os.path.join(DATA_DIR, 'experiment-raw-results.csv')
OUTPUT_JSON = os.path.join(DATA_DIR, 'confusion-matrices.json')

FIELDNAMES = ['doc_id', 'company', 'sector', 'true_label', 'condition',
              'rater', 'detected_label', 'confidence', 'time_minutes', 'reasoning']


def load_corpus():
    with open(INPUT_CSV, 'r') as f:
        return list(csv.DictReader(f))


def save_results_csv(results):
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} rows to {OUTPUT_CSV}")


def save_metrics_json(output):
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Saved metrics to {OUTPUT_JSON}")
