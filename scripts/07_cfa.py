"""07_cfa.py — confirmatory factor analysis on CSA (4 items). Uses semopy."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)

try:
    from semopy import Model
    from semopy.stats import calc_stats
except Exception:
    Model = None


def main() -> None:
    if Model is None:
        print("semopy is not installed. Run:  pip install semopy")
        return

    b = pd.read_csv(DATA / "dataset_B_indices.csv")
    items = b[["csa_school", "csa_role", "csa_imp", "csa_local"]].dropna()
    print(f"CFA on N = {len(items)} complete cases")

    spec = """
    CSA =~ csa_school + csa_role + csa_imp + csa_local
    """
    m = Model(spec)
    m.fit(items, obj="MLW")
    est = m.inspect()
    est.to_csv(RES / "cfa_csa_estimates.csv", index=False)
    print(est.to_string(index=False))

    try:
        stats = calc_stats(m)
        stats.to_csv(RES / "cfa_csa_fit.csv")
        print("\nFit indices:")
        print(stats)
    except Exception as e:
        print("Fit-index calculation skipped:", e)


if __name__ == "__main__":
    main()
