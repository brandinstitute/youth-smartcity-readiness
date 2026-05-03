"""03_regressions.py — Models 7.1 (AEI) and 7.2 (CSA).

Both models are fit twice:
  (a) classic OLS for the published coefficient table;
  (b) OLS with HC3 heteroscedasticity-consistent (sandwich) standard errors as
      a robustness check, written to *_robust.txt next to the main outputs.
The classical fit is what appears in Tables in Chapter 7 of the monograph; the
HC3 fit confirms that significance levels do not hinge on the homoscedasticity
assumption. Reported in the replication note attached to §7.4.
"""
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
    fit1_hc3 = sm.OLS(m1["AEI"], X1).fit(cov_type="HC3")
    (RES / "model_7_1_AEI.txt").write_text(str(fit1.summary()))
    (RES / "model_7_1_AEI_robust.txt").write_text(str(fit1_hc3.summary()))

    b = pd.read_csv(DATA / "dataset_B_indices.csv")
    b["Female"] = (b["gender"] == "Žena").astype(int)
    m2 = b[["CSA", "DAE", "SDR", "Female", "grade_int"]].dropna().rename(columns={"grade_int": "Grade"})
    X2 = sm.add_constant(m2[["DAE", "SDR", "Female", "Grade"]])
    fit2 = sm.OLS(m2["CSA"], X2).fit()
    fit2_hc3 = sm.OLS(m2["CSA"], X2).fit(cov_type="HC3")
    (RES / "model_7_2_CSA.txt").write_text(str(fit2.summary()))
    (RES / "model_7_2_CSA_robust.txt").write_text(str(fit2_hc3.summary()))

    print("Model 7.1 (AEI): N =", len(m1), " R^2 =", round(fit1.rsquared, 3))
    print(fit1.summary().tables[1])
    print("Model 7.1 — HC3 robust SE coefficient table:")
    print(fit1_hc3.summary().tables[1])
    print("\nModel 7.2 (CSA): N =", len(m2), " R^2 =", round(fit2.rsquared, 3))
    print(fit2.summary().tables[1])
    print("Model 7.2 — HC3 robust SE coefficient table:")
    print(fit2_hc3.summary().tables[1])


if __name__ == "__main__":
    main()
