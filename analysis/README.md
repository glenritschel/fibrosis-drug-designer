# analysis — reproducibility code and data

Code and data behind the preprint *"Localization, not selectivity: a causal
target–tissue–outcome framework for designing tissue-directed multikinase
anti-fibrotics"* (Zenodo: [10.5281/zenodo.21681579](https://doi.org/10.5281/zenodo.21681579))
and its companion US provisional patent specification
(Zenodo: [10.5281/zenodo.21681253](https://doi.org/10.5281/zenodo.21681253);
US Application 64/120,995).

The interactive tool (`../index.html`) and the explainer animation (`../manim/`)
live in the repository root. This folder is the non-interactive analysis.

## Contents

| File | What it does |
|---|---|
| `optimization_analysis.py` | Exhaustive target-set × delivery-route optimization (508 designs). Writes `results/optimization_results.json`. |
| `validate_and_screen.py` | Validates the 10 candidate SMILES against their PubChem molecular formula/weight (RDKit), then runs the developability screen. Writes `candidates.csv` and `results/developability_results.csv`. |
| `developability_screen.py` | Standalone developability pipeline (RDKit) over `candidates.csv`. |
| `make_figure.py` | Renders `results/optimization_figure.png`. |
| `make_structures_grid.py` | Renders `results/candidate_structures.png`. |
| `candidates.csv` | The 10 candidate agents with PubChem-verified SMILES + CIDs. |
| `reinvent4_fibrotic_scoring.toml` | REINVENT4 scoring specification for the de-novo (single-molecule) path. |
| `METHODS.md` | The in-silico support dossier: methods, results, protocols, sources. |
| `HOW_TO_populate_candidates.md` | How the candidate SMILES were sourced and verified from PubChem. |
| `results/` | Generated outputs (JSON, CSV, figures). |

## Reproduce

```bash
pip install -r requirements.txt
python validate_and_screen.py     # SMILES validation + developability table
python optimization_analysis.py   # route optima over 508 designs
python make_figure.py             # optimization figure
python make_structures_grid.py    # structures grid
```

## Notes

The per-target efficacy weights and severities are **illustrative heuristics** for
exploring trade-offs, not measured pharmacology. The *structure* of the
conclusions (which target each localized route must drop; that no systemic design
avoids the serious effects) is robust; the specific numbers are not. Candidate
SMILES were retrieved from PubChem and validated in RDKit (formula and molecular
weight match). No wet-laboratory data is included. See `METHODS.md` and the
preprint for full framing and limitations.
