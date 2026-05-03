"""02_descriptives.py — descriptive tables (Tables 1–11 of the monograph)."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)


def desc(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce").dropna()
    return {"N": len(s), "mean": round(s.mean(), 2), "sd": round(s.std(), 2),
            "min": round(s.min(), 2), "q25": round(s.quantile(.25), 2),
            "median": round(s.median(), 2), "q75": round(s.quantile(.75), 2),
            "max": round(s.max(), 2)}


def main() -> None:
    a = pd.read_csv(DATA / "dataset_A_indices.csv")
    b = pd.read_csv(DATA / "dataset_B_indices.csv")

    rows_A = [{"Index": k, **desc(a[k])} for k in
              ["time_h", "inst", "used", "use_ratio", "AEI"]]
    pd.DataFrame(rows_A).to_csv(RES / "table_A_descriptives.csv", index=False)

    rows_B = [{"Index": k, **desc(b[k])} for k in
              ["DAE", "SDR", "CSA", "YSCR"]]
    pd.DataFrame(rows_B).to_csv(RES / "table_B_descriptives.csv", index=False)

    print(pd.DataFrame(rows_A).to_string(index=False))
    print()
    print(pd.DataFrame(rows_B).to_string(index=False))


if __name__ == "__main__":
    main()
