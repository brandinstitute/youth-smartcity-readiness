"""06_bootstrap_ci.py — bootstrap 95% CI for key means (Dataset A and B)."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)


def boot_ci(values, n_boot: int = 2000, ci: float = 95, seed: int = 42):
    rng = np.random.default_rng(seed)
    v = pd.Series(values).dropna().to_numpy()
    if len(v) < 2:
        return None, None, None, None
    boots = rng.choice(v, size=(n_boot, len(v)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    return float(v.mean()), float(lo), float(hi), len(v)


def main() -> None:
    a = pd.read_csv(DATA / "dataset_A_indices.csv")
    b = pd.read_csv(DATA / "dataset_B_indices.csv")

    rows = []
    for label, col in [("daily_time_h", a["time_h"]),
                       ("apps_installed", a["inst"]),
                       ("apps_used", a["used"]),
                       ("use_ratio", a["use_ratio"]),
                       ("AEI", a["AEI"]),
                       ("DAE", b["DAE"]),
                       ("SDR", b["SDR"]),
                       ("CSA", b["CSA"]),
                       ("YSCR", b["YSCR"])]:
        m, lo, hi, n = boot_ci(col)
        rows.append({"variable": label, "N": n,
                     "mean": round(m, 2), "lo95": round(lo, 2), "hi95": round(hi, 2)})

    out = pd.DataFrame(rows)
    out.to_csv(RES / "bootstrap_ci.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
