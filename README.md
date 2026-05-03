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
| `data/.gitkeep` | Place source surveys here (not committed — see `data/README.md`) |
| `results/.gitkeep` | Generated outputs land here |
| `docs/codebook.md` | Variable-by-variable codebook for both surveys |
| `docs/foreword_request_email.md` | Template e-mail for inviting an external author of the foreword |

## Repository layout

```
.
├── data/                          # source surveys (not committed)
│   ├── results-survey777777__2_.csv
│   ├── results-survey971496.csv
│   └── people-smart-cities-indikatory-slovensko.xlsx
├── scripts/                       # Python analysis scripts (7 files)
├── notebooks/                     # exploratory notebooks (optional)
├── results/                       # generated tables and figures
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

# 3. Place the three source files into ./data/
#    - results-survey777777__2_.csv      (Dataset A — mobile habits)
#    - results-survey971496.csv          (Dataset B — smart-city perception)
#    - people-smart-cities-indikatory-slovensko.xlsx  (Slovak indicators)

# 4. Run the full pipeline
python scripts/01_build_indices.py
python scripts/02_descriptives.py
python scripts/03_regressions.py
python scripts/04_clusters.py
python scripts/05_sensitivity_pca.py
python scripts/06_bootstrap_ci.py
python scripts/07_cfa.py
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

- **Code** (`scripts/`, `notebooks/`): MIT License (see `LICENSE`).
- **Documentation and metadata** (`docs/`, `README.md`, `CITATION.cff`): Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Aggregated, anonymised data** (if released): Creative Commons Attribution 4.0 International (CC BY 4.0).

## Contact

Andrej Kóňa, PhD.
Faculty of Social Sciences
University of Ss. Cyril and Methodius in Trnava
Email: andrej.kona@ucm.sk
