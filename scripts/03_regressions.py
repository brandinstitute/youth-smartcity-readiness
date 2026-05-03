"""03_regressions.py — Models 7.1 (AEI) and 7.2 (CSA)."""
from pathlib import Path
import pandas as pd
import statsmodels.api as sm

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)


def main() -> None:
    a = pd.read_csv(DATA / "dataset_A_indices.csv")
    a["Female"] = (a["gender"] == "Žena").astype(int)
    a["iOS"] = (a["os"] == "iOS").astype(int)
    a["Age"] = pd.to_numeric(a["age"], errors="coerce")

    m1 = a[["AEI", "motives_count", "Female", "Age", "iOS"]].dropna()
    X1 = sm.add_constant(m1[["motives_count", "Female", "Age", "iOS"]])
    fit1 = sm.OLS(m1["AEI"], X1).fit()
    with open(RES / "model_7_1_AEI.txt", "w") as f:
        f.write(str(fit1.summary()))

    b = pd.read_csv(DATA / "dataset_B_indices.csv")
    b["Female"] = (b["gender"] == "Žena").astype(int)
    m2 = b[["CSA", "DAE", "SDR", "Female", "grade_int"]].dropna().rename(columns={"grade_int": "Grade"})
    X2 = sm.add_constant(m2[["DAE", "SDR", "Female", "Grade"]])
    fit2 = sm.OLS(m2["CSA"], X2).fit()
    with open(RES / "model_7_2_CSA.txt", "w") as f:
        f.write(str(fit2.summary()))

    print("Model 7.1 (AEI): N =", len(m1), " R^2 =", round(fit1.rsquared, 3))
    print(fit1.summary().tables[1])
    print("\nModel 7.2 (CSA): N =", len(m2), " R^2 =", round(fit2.rsquared, 3))
    print(fit2.summary().tables[1])


if __name__ == "__main__":
    main()
