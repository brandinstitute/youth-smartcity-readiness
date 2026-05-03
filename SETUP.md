# Setup — krok-za-krokom pre Windows / macOS / Linux

This guide takes a fresh machine to a working replication environment in about ten minutes, then walks you through publishing the package on GitHub and minting a Zenodo DOI.

---

## A. Local pipeline — Windows (PowerShell)

```powershell
cd <path\to\your\clone>\youth-smartcity-readiness

# Copy the three source files into ./data/
Copy-Item "<path\to>\results-survey777777 (2).csv"    -Destination ".\data\"
Copy-Item "<path\to>\results-survey971496.csv"        -Destination ".\data\"
Copy-Item "<path\to>\people-smart-cities-indikatory-slovensko.xlsx" -Destination ".\data\"

# Python environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the pipeline
python scripts\01_build_indices.py
python scripts\02_descriptives.py
python scripts\03_regressions.py
python scripts\04_clusters.py
python scripts\05_sensitivity_pca.py
python scripts\06_bootstrap_ci.py
python scripts\07_cfa.py
```

If Python is not installed: download Python 3.11 from <https://www.python.org/downloads/> and tick "Add Python to PATH" in the installer.

## A.bis Local pipeline — macOS / Linux

```bash
cd /path/to/youth-smartcity-readiness

cp /path/to/results-survey777777\ \(2\).csv data/
cp /path/to/results-survey971496.csv data/
cp /path/to/people-smart-cities-indikatory-slovensko.xlsx data/

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

for s in scripts/*.py; do python "$s"; done
```

---

## B. Publish on GitHub (account `brandinstitute`)

Create a new repository on GitHub.com:

- <https://github.com/new>
- Owner: `brandinstitute`
- Repository name: `youth-smartcity-readiness`
- Public, no README/LICENSE/.gitignore (we already have these locally)

Then push from PowerShell:

```powershell
git config --global user.name "Andrej Kóňa"
git config --global user.email "andrej.kona@ucm.sk"

git init
git add .
git commit -m "Initial release: replication code for YSCR monograph"
git branch -M main
git remote add origin https://github.com/brandinstitute/youth-smartcity-readiness.git
git push -u origin main
```

GitHub will prompt for a Personal Access Token (PAT) — generate one at <https://github.com/settings/tokens> → "Generate new token (classic)" → scope `repo`.

---

## C. Mint a Zenodo DOI

1. Go to <https://zenodo.org/account/settings/github/>.
2. Sign in with the GitHub account that owns the repository (`brandinstitute`).
3. Find `youth-smartcity-readiness` in the list and toggle the switch **ON**.
4. Back on GitHub, create a release:
   - <https://github.com/brandinstitute/youth-smartcity-readiness/releases/new>
   - Tag: `v1.0.0`
   - Title: `v1.0.0 — Initial replication release`
   - Description: short summary (1–2 sentences) of what is included.
5. Click **Publish release**.
6. After 1–2 minutes Zenodo creates a DOI of the form `10.5281/zenodo.XXXXXXX`.

---

## D. Update the DOI in the monograph

Once the DOI is minted, insert it in:

- The Acknowledgments / Data availability statement of the monograph (front matter and §4.3).
- The `CITATION.cff` (under `identifiers:`).
- Any internal cross-reference that currently reads "DOI to be supplied".

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: pandas` | Virtual environment not activated | Re-run the activate command for your shell |
| `FileNotFoundError: data/results-survey...` | Source files not yet placed in `./data/` | See section A |
| `UnicodeDecodeError` on CSV read | Wrong encoding | The scripts default to UTF-8 with `;` as delimiter; if your export differs, edit the `pd.read_csv` call in `01_build_indices.py` |
| `semopy` install fails on Windows | Missing C++ build tools | Install Microsoft C++ Build Tools, or skip `07_cfa.py` — the rest of the pipeline does not need semopy |
| `git push` rejected as non-fast-forward | Remote already has commits | `git pull --rebase origin main` and re-push |
| Zenodo does not appear after release | Integration not toggled before the release | Toggle ON, delete the release on GitHub, create a new release with a new tag (e.g. `v1.0.1`) |

## Updating the package

```bash
pip install --upgrade -r requirements.txt
```

If a major version of any dependency moves and a script breaks, please open an issue with the version pair (old → new) and the traceback.
