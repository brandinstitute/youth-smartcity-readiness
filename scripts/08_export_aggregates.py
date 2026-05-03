"""08_export_aggregates.py — produce anonymised, aggregate-only CSV files.

These files are safe to commit to the public repository (CC BY 4.0). They
contain NO individual-level rows — only sample-level descriptive statistics,
correlation matrices and group means that already appear in the published
monograph.

Outputs land in `data/aggregates/`. The folder is whitelisted in `.gitignore`
so that committing it does not accidentally bring raw CSVs along.

Run AFTER scripts 01–06 because it reuses dataset_A_indices.csv and
dataset_B_indices.csv produced by 01_build_indices.py and the bootstrap /
sensitivity outputs from 05 and 06.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AGG = DATA / "aggregates"
AGG.mkdir(parents=True, exist_ok=True)
RES = ROOT / "results"


def desc(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce").dropna()
    return {
        "N": int(len(s)),
        "mean": round(float(s.mean()), 3),
        "sd": round(float(s.std()), 3),
        "min": round(float(s.min()), 3),
        "q25": round(float(s.quantile(0.25)), 3),
        "median": round(float(s.median()), 3),
        "q75": round(float(s.quantile(0.75)), 3),
        "max": round(float(s.max()), 3),
    }


def export_dataset_A(a: pd.DataFrame) -> None:
    rows = [{"variable": k, **desc(a[k])} for k in
            ["time_h", "inst", "used", "use_ratio", "AEI"]]
    pd.DataFrame(rows).to_csv(AGG / "dataset_A_aggregates.csv", index=False)

    motive_cols = ["m_peer", "m_family", "m_ads", "m_curiosity",
                   "m_school", "m_entertain", "m_trend"]
    motives = []
    n = len(a)
    for c in motive_cols:
        cnt = int(pd.to_numeric(a[c], errors="coerce").fillna(0).astype(int).sum())
        motives.append({"motive": c, "count": cnt, "pct_of_N": round(100 * cnt / n, 2), "N_sample": n})
    pd.DataFrame(motives).to_csv(AGG / "dataset_A_motives.csv", index=False)

    feats = ["AEI", "motives_count", "m_entertain", "m_school", "m_trend", "m_curiosity"]
    sub = a[feats].dropna().copy()
    X = StandardScaler().fit_transform(sub)
    km = KMeans(n_clusters=4, random_state=42, n_init=20).fit(X)
    sub["cluster"] = km.labels_
    profile = sub.groupby("cluster").mean().round(3)
    profile["N"] = sub.groupby("cluster").size().astype(int)
    profile["pct"] = (100 * profile["N"] / len(sub)).round(2)
    profile = profile.reset_index()
    profile.to_csv(AGG / "dataset_A_segments_k4.csv", index=False)

    diag = []
    for k in range(2, 7):
        m = KMeans(n_clusters=k, random_state=42, n_init=20).fit(X)
        diag.append({"k": k, "silhouette": round(float(silhouette_score(X, m.labels_)), 3)})
    pd.DataFrame(diag).to_csv(AGG / "dataset_A_segment_diagnostics.csv", index=False)


def export_dataset_B(b: pd.DataFrame) -> None:
    rows = [{"index": k, **desc(b[k])} for k in ["DAE", "SDR", "CSA", "YSCR"]]
    if "YSCR_listwise" in b.columns:
        rows.append({"index": "YSCR_listwise", **desc(b["YSCR_listwise"])})
    pd.DataFrame(rows).to_csv(AGG / "dataset_B_aggregates.csv", index=False)

    corr = b[["DAE", "SDR", "CSA", "YSCR"]].corr().round(3)
    corr.to_csv(AGG / "dataset_B_correlations.csv")

    by_grade = (b.groupby("grade_int")[["DAE", "SDR", "CSA", "YSCR"]]
                .agg(["mean", "std", "count"]).round(3))
    by_grade.to_csv(AGG / "dataset_B_by_grade.csv")

    if "gender" in b.columns:
        by_gender = (b.groupby("gender")[["DAE", "SDR", "CSA", "YSCR"]]
                     .agg(["mean", "std", "count"]).round(3))
        by_gender.to_csv(AGG / "dataset_B_by_gender.csv")


def export_municipal(src_xlsx: Path) -> None:
    if not src_xlsx.exists():
        print(f"  [skip] {src_xlsx.name} not present in data/, municipal aggregate not exported")
        return
    raw = pd.read_excel(src_xlsx, sheet_name=0, header=None)
    header_row = raw.iloc[3].tolist()
    data = raw.iloc[4:].copy()
    data.columns = header_row
    keep = data.iloc[:, :4].copy()
    keep.columns = ["municipality", "okres", "kraj", "population"]
    indicator_cols = data.columns[4:]
    z = data[indicator_cols].apply(pd.to_numeric, errors="coerce")
    keep["smart_people_zmean"] = z.mean(axis=1, skipna=True).round(4)
    keep["smart_people_n_indicators"] = z.notna().sum(axis=1).astype(int)
    keep.to_csv(AGG / "municipalities_smart_people.csv", index=False)


def copy_pipeline_outputs() -> None:
    # bootstrap CIs and YSCR sensitivity already produced in /results by scripts 05 & 06.
    for src_name in ("bootstrap_ci.csv",
                     "yscr_sensitivity_descriptives.csv",
                     "yscr_sensitivity_correlations.csv",
                     "cluster_diagnostics.csv",
                     "cluster_profiles_k4.csv"):
        src = RES / src_name
        if src.exists():
            (AGG / src_name).write_bytes(src.read_bytes())


def main() -> None:
    a_path = DATA / "dataset_A_indices.csv"
    b_path = DATA / "dataset_B_indices.csv"
    if not a_path.exists() or not b_path.exists():
        raise SystemExit("Run scripts/01_build_indices.py first.")
    a = pd.read_csv(a_path)
    b = pd.read_csv(b_path)
    export_dataset_A(a)
    export_dataset_B(b)
    export_municipal(DATA / "people-smart-cities-indikatory-slovensko.xlsx")
    copy_pipeline_outputs()
    print(f"Aggregates written to {AGG}")
    for f in sorted(AGG.iterdir()):
        if f.is_file():
            print(f"  - {f.name}  ({f.stat().st_size} B)")


if __name__ == "__main__":
    main()
