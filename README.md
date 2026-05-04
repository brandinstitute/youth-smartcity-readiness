# Youth Smart-City Readiness — replication package

Replication code and documentation for the monograph:

> Kóňa, A., & Cagáňová, D. (2026). *Digital Habits and Smart-City Readiness of Secondary-School Students: Bridging Mobile Ecosystems and Civic Digital Literacy.* Springer Nature / EAI Publishing. ISBN to be supplied. DOI to be supplied.

The volume is the empirical and conceptual output of the **KEGA 004UCM-4/2023 project "Education for Smart Slovakia"**.

## What this repository contains

Scripts that reproduce every empirical figure, table and index reported in Chapters 5–8 of the monograph from two anonymous student surveys (Datasets A and B) and a municipal-level indicator file for Slovakia.

| Asset | Contents |
|---|---|
| `scripts/01_build_indices.py` | Constructs the four composite indices: AEI, DAE, SDR, CSA, and the YSCR aggregate |
| `scripts/02_descriptives.py` | Tables 1–11 (sample profile, time, installed/used apps, motives, top apps) |
| `scripts/03_regressions.py` | OLS Models 7.1 and 7.2 with full diagnostics |
| `scripts/04_clusters.py` | k-means clustering (k = 2 … 6) underlying the four youth personas |
| `scripts/05_sensitivity_pca.py` | YSCR robustness check across default, equal and PCA-based weights |
| `scripts/06_bootstrap_ci.py` | 95 % bootstrap confidence intervals for all index means |
| `scripts/07_cfa.py` | Confirmatory factor analysis on the SDR and CSA item batteries (semopy) |
| `scripts/08_export_aggregates.py` | Writes the anonymised CSV companions to `data/aggregates/` (CC BY 4.0) |
| `scripts/09_parse_lss.py` | Parses LimeSurvey `.lss` exports into the Slovak Markdown source for Appendix A |
| `scripts/10_insert_appendix_a.py` | Embeds the Appendix-A markdown into the monograph (`.docx`) with proper headings |
| `scripts/11_fill_appendices.py` | Fills Appendices B/C/D/E with native Word tables sourced from `data/aggregates/` |
| `scripts/12_make_figures.py` | Renders Figure 1 (conceptual model) and Figure 2 (4-panel histograms) as PNG |
| `scripts/13_fix_monografia.py` | One-off recovery script — fixes "delete-only" edits left in an earlier draft |
| `data/README.md` | How to obtain the raw surveys (kept locally, not committed) |
| `data/aggregates/` | Public, citable aggregate CSVs that mirror the published tables (CC BY 4.0) |
| `results/.gitkeep` | Generated tables, figures and patched .docx files land here (gitignored) |
| `docs/codebook.md` | Variable-by-variable codebook for both surveys |
| `docs/foreword_request_email.md` | Template e-mail for inviting an external author of the foreword |

## Repository layout

```
.
├── data/
│   ├── README.md                  # how to obtain raw surveys (raw files are gitignored)
│   └── aggregates/                # CC BY 4.0 — anonymised companion CSVs
│       ├── README.md
│       ├── LICENSE-CC-BY-4.0.md
│       └── *.csv (14 files: descriptives, correlations, clusters, bootstrap, sensitivity, municipal)
├── scripts/                       # Python analysis & monograph-build scripts (13 files)
├── results/                       # generated tables, figures and patched .docx files (gitignored)
├── docs/
│   ├── codebook.md
│   └── foreword_request_email.md
├── .github/workflows/zenodo.yml
├── requirements.txt
├── LICENSE
├── CITATION.cff
├── SETUP.md
└── README.md
```

## Quick start

```bash
# 1. Clone or unzip this repository
git clone https://github.com/brandinstitute/youth-smartcity-readiness.git
cd youth-smartcity-readiness

# 2. Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt

# 3. Place the source files into ./data/
#    Required for the analytic pipeline (steps 01–08):
#      - results-survey777777 (2).csv         (Dataset A — mobile habits)
#      - results-survey971496.csv             (Dataset B — smart-city perception)
#      - people-smart-cities-indikatory-slovensko.xlsx  (Slovak indicators)
#    Optional for the monograph-build pipeline (steps 09–13):
#      - limesurvey_survey_777777.lss         (Dataset A questionnaire export, for Appendix A)
#      - limesurvey_survey_971496.lss         (Dataset B questionnaire export, for Appendix A)
#      - monograph_in.docx                    (current draft of the manuscript)

# 4. Analytic pipeline
python scripts/01_build_indices.py
python scripts/02_descriptives.py
python scripts/03_regressions.py
python scripts/04_clusters.py
python scripts/05_sensitivity_pca.py
python scripts/06_bootstrap_ci.py
python scripts/07_cfa.py
python scripts/08_export_aggregates.py   # rebuilds data/aggregates/

# 5. Optional: monograph-build pipeline (regenerate Appendices and figures)
python scripts/09_parse_lss.py            # → results/Appendix_A_Dataset_*.md
python scripts/10_insert_appendix_a.py    # → results/monograph_with_appendix_a.docx
python scripts/11_fill_appendices.py      # → results/monograph_with_appendices.docx
python scripts/12_make_figures.py         # → results/Figure_1_*.png, Figure_2_*.png
# python scripts/13_fix_monografia.py     # one-off recovery script — read first
```

All outputs land in `./results/` as `.csv`, `.json` and `.txt` files keyed to the table or section they support in the monograph.

For step-by-step Windows / GitHub / Zenodo instructions, see `SETUP.md`.

## Citing this work

```
Kóňa, A., & Cagáňová, D. (2026). Digital Habits and Smart-City Readiness of
Secondary-School Students: Bridging Mobile Ecosystems and Civic Digital
Literacy. Springer Nature / EAI Publishing. ISBN to be supplied. DOI to be
supplied.
```

Use `CITATION.cff` for automated citation tools.

## Data ethics

The raw, individual-level survey responses are not redistributed under this licence. The original questionnaires were administered as anonymous online surveys with informed consent at the school level; participation was voluntary. See §4.3 of the monograph for the full ethics statement.

The three source files are available on request from the corresponding author for purposes of academic replication, subject to a data-use agreement consistent with the original consent obtained from participants and from the head teachers of participating schools.

## Reproducibility notes

- All scripts are deterministic given the same `numpy` random seed (`SEED = 42`), set at the top of each file that uses random sampling (clusters, bootstrap).
- The OLS, k-means and PCA results in the monograph were generated on Python 3.11 with the package versions pinned in `requirements.txt`.
- The replication code in this repository implements the index-construction logic described in §4.4 of the monograph. Minor differences in N and point estimates between the published tables and the script outputs reflect alternative listwise-deletion conventions and edge-case handling, and are documented in `docs/codebook.md`.
- If your re-run produces values that disagree with the script's first run beyond the third decimal place, please open an issue.

## Versioning

This package is versioned with [Semantic Versioning](https://semver.org/). A persistent DOI is issued via Zenodo upon each tagged release (see `.github/workflows/zenodo.yml` and the Zenodo section of `SETUP.md`).

## Licence

- **Code and documentation** (`scripts/`, `docs/`, `README.md`, `SETUP.md`, `CITATION.cff`, the root `LICENSE`): MIT License — see `LICENSE`.
- **Aggregated, anonymised data** in `data/aggregates/`: Creative Commons Attribution 4.0 International (CC BY 4.0). The licence text is in `data/aggregates/LICENSE-CC-BY-4.0.md`. The aggregates are sample-level summaries derived from the original surveys; no individual-level rows are released.

## Contact

Andrej Kóňa, PhD.
Faculty of Social Sciences
University of Ss. Cyril and Methodius in Trnava
Email: andrej.kona@ucm.sk
