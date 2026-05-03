# Source data — placement and access

This folder is intentionally empty in the public repository. The original survey responses are not redistributed here, in line with the school-level data-protection commitments described in §4.3 of the monograph.

## How to obtain the source files

Three files are needed to run the pipeline:

| File | Description | Notes |
|---|---|---|
| `results-survey777777 (2).csv` | Dataset A — mobile-app habits (LimeSurvey export, `;`-separated, UTF-8 with BOM) | 135 raw rows; 82 secondary-school cases used in the monograph |
| `results-survey971496.csv` | Dataset B — digital environment and smart-city literacy (LimeSurvey export) | 833 raw rows; 401 completed; 368 in mainstream grades 1–4 |
| `people-smart-cities-indikatory-slovensko.xlsx` | Slovak municipal indicators (z-scored Boyd-Cohen "Smart People" components) | 253 municipalities, ~3.33 M residents |

Researchers wishing to replicate the analyses can request these files from the corresponding author for academic, non-commercial purposes, subject to a short data-use agreement consistent with the original consent obtained from participants and head teachers. Aggregated anonymised data may be released as a separate Zenodo deposit in the future.

## Generated files (created by the scripts, not version-controlled)

When you run `scripts/01_build_indices.py` the following are produced in this folder:

- `dataset_A_indices.csv` — Dataset A with derived indices (AEI, motives, use_ratio).
- `dataset_B_indices.csv` — Dataset B with derived indices (DAE, SDR, CSA, YSCR, YSCR_listwise).

Both are listed in `.gitignore` and never reach the public repo.

## Contact

Andrej Kóňa, PhD. — andrej.kona@ucm.sk
Faculty of Social Sciences, University of Ss. Cyril and Methodius in Trnava.
