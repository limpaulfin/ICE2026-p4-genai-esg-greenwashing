# ICE2026-p4-genai-esg-greenwashing

Companion code and processed data for the ICE 2026 paper *From Greenwashing to Algorithmic Assurance: Evaluating Generative AI for ESG Reporting Transparency* (manuscript 1034, HUIT Journal of Science Special Issue).

## Summary

Pipeline that pairs a Retrieval-Augmented Generation layer with a baseline Large Language Model and measures their relative ability to flag misleading sustainability claims across thirty-five labelled excerpts. Outputs include the per-document classification trace, confusion matrices, McNemar test artefacts, Bayesian posterior summaries, and the figures shipped with the manuscript.

## Repository layout

- `src/python/` — module-level pipeline (`m01_evidence` … `m06_run`). Used by the experiment driver.
- `src/scripts/` — runnable entry points (`run_experiment.py`, `task13-detection-rate-analysis.py`, figure generators).
- `src/R/` — placeholder for follow-up R analyses.
- `data/` — processed datasets only (no raw artefacts, no PII). Includes `esg-corpus-metadata.csv` (per-document labels), the experiment outputs, and the cleaned World Bank context series.
- `docs/annotation-taxonomy.md` — labelling rubric reference.
- `prompts/` — reserved for prompt template sharing in a follow-up release.

## Requirements

- Linux (tested on Debian 12 / Ubuntu 22.04).
- Python 3.12.
- An OpenAI-compatible API key for `GPT-4o-mini` set via the `OPENAI_API_KEY` environment variable.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib scipy openai
```

## Run

```bash
export OPENAI_API_KEY=<your_key>
python src/scripts/run_experiment.py             # writes confusion + metrics
python src/scripts/task13-detection-rate-analysis.py
python src/scripts/gen_fig_detection.py          # rebuilds detection-comparison.png
```

## Data origin

- Greenwashing corpus seeds: GreenClaims (Kaggle, CC; user `DizzyPanda1`).
- Environmental context: World Bank Open Data (`https://data.worldbank.org`).
- Simulated reports: nineteen entries generated from public sustainability templates following the protocol described in `docs/annotation-taxonomy.md`. The split is sixteen real and nineteen simulated documents (forty-six and fifty-four percent respectively).

## Citation

```bibtex
@inproceedings{p4_2026_genai_esg_greenwashing,
  title     = {From Greenwashing to Algorithmic Assurance: Evaluating Generative AI for ESG Reporting Transparency},
  booktitle = {Proceedings of the 3rd International Conference on Economics (ICE 2026)},
  year      = {2026},
  publisher = {HUIT Journal of Science Special Issue}
}
```

## License

MIT. See `LICENSE`.
