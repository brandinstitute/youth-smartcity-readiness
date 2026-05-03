"""
01_build_indices.py — REFERENCE IMPLEMENTATION

Builds AEI, DAE, SDR, CSA, YSCR indices reported in the monograph.
Reproduces the exact N values from the published tables.

Reads:  data/results-survey777777 (2).csv  (Dataset A)
        data/results-survey971496.csv      (Dataset B)
Writes: data/dataset_A_indices.csv         (N = 82, AEI valid = 77)
        data/dataset_B_indices.csv         (N = 368, YSCR valid = 368)
"""
from __future__ import annotations
import re
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"


def zscore(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce")
    sd = x.std()
    return (x - x.mean()) / sd if sd else x * 0


def minmax(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce")
    rng = x.max() - x.min()
    return 100 * (x - x.min()) / rng if rng else x * 0


def to_int_dev(x):
    if pd.isna(x):
        return np.nan
    m = re.search(r"\d+", str(x))
    if m:
        n = int(m.group())
        if 0 <= n <= 30:
            return n
    return np.nan


def build_dataset_A() -> pd.DataFrame:
    df = pd.read_csv(DATA / "results-survey777777 (2).csv", sep=None, engine="python")
    df = df[df["submitdate. Dátum odoslania"].notna()].copy()
    df = df.rename(columns={
        "POHLAVIE. Pohlavie:": "gender",
        "VEK. Vek:": "age",
        "TYPSKOLY. Typ školy:": "school_type",
        "OS. Operačný systém mobilu:": "os",
        "POCETAPLIK. Koľko máte aktuálne nainštalovaných aplikácií (odhad):": "apps_installed",
        "POCETAPLIKpouzivam. Koľko používate aspoň raz z nainštalovaných aplikácií (odhad):": "apps_used",
        "G02Q51. Priemerný čas používania aplikácií denne (okrem hovorov a SMS):": "time_daily",
        "G02Q52. Kedy ste si naposledy nainštalovali novú aplikáciu?": "last_install",
    })
    ss = df[df["school_type"] == "Stredná škola"].copy()

    TIME = {"Menej ako 1 hodinu": 0.5, "1-3 hodiny": 2.0, "3-5 hodín": 4.0, "Viac ako 5 hodín": 6.0}
    LAST = {"Tento týždeň": 3, "Tento mesiac": 2, "Viac ako pred mesiacom": 1}
    ss["time_h"] = ss["time_daily"].map(TIME)
    ss["last_n"] = ss["last_install"].map(LAST)
    ss["inst"] = pd.to_numeric(ss["apps_installed"], errors="coerce")
    ss["used"] = pd.to_numeric(ss["apps_used"], errors="coerce")
    ss["use_ratio"] = ss["used"] / ss["inst"]

    ss["c_time"] = minmax(ss["time_h"])
    ss["c_inst"] = minmax(ss["inst"])
    ss["c_recency"] = minmax(ss["last_n"])
    ss["AEI"] = 0.5 * ss["c_time"] + 0.3 * ss["c_inst"] + 0.2 * ss["c_recency"]

    motive_cols = {
        "G01Q53[SQ001]. Prečo si inštalujete nové aplikácie? [Odporúčanie spolužiaka / kamaráta]": "m_peer",
        "G01Q53[SQ002]. Prečo si inštalujete nové aplikácie? [Odporúčanie člena rodiny]": "m_family",
        "G01Q53[SQ003]. Prečo si inštalujete nové aplikácie? [Reklama (YouTube, Instagram, TikTok, atď.)]": "m_ads",
        "G01Q53[SQ004]. Prečo si inštalujete nové aplikácie? [Zvedavosť / chcem skúšať nové veci]": "m_curiosity",
        "G01Q53[SQ005]. Prečo si inštalujete nové aplikácie? [Potrebujem ju do školy / práce]": "m_school",
        "G01Q53[SQ006]. Prečo si inštalujete nové aplikácie? [kvôli zábave]": "m_entertain",
        "G01Q53[SQ007]. Prečo si inštalujete nové aplikácie? [kvôli móde / trendom]": "m_trend",
    }
    for col, alias in motive_cols.items():
        ss[alias] = (ss[col] == "Áno").astype(int)
    ss["motives_count"] = ss[list(motive_cols.values())].sum(axis=1)

    out_cols = ["gender", "age", "os", "time_h", "inst", "used", "use_ratio",
                "c_time", "c_inst", "c_recency", "AEI", "motives_count"] + list(motive_cols.values())
    return ss[out_cols].reset_index(drop=True)


def build_dataset_B() -> pd.DataFrame:
    df = pd.read_csv(DATA / "results-survey971496.csv", sep=None, engine="python")
    df = df[df["submitdate. Dátum odoslania"].notna()].copy()

    def col(prefix: str):
        for c in df.columns:
            if c.startswith(prefix + ".") or c.startswith(prefix + "["):
                return c
        return None

    rename = {}
    codes = {
        "G02Q02": "grade", "G01Q03": "gender", "G01Q10": "sc_role_tech",
        "G05Q18": "encountered_local", "G01Q22": "sc_at_school", "G01Q23": "sc_importance_edu",
    }
    for code, alias in codes.items():
        c = col(code)
        if c:
            rename[c] = alias
    ratings = {"G01Q26[SQ001]": "q_school", "G01Q26[SQ002]": "q_home",
               "G01Q26[SQ003]": "q_city", "G01Q26[SQ004]": "q_equip"}
    devs = {"G08Q25[SQ001]": "dev_mobile", "G08Q25[SQ002]": "dev_media",
            "G08Q25[SQ003]": "dev_compute", "G08Q25[SQ004]": "dev_iot"}
    for code, alias in {**ratings, **devs}.items():
        for c in df.columns:
            if c.startswith(code):
                rename[c] = alias
                break

    df = df.rename(columns=rename)
    df["grade_int"] = pd.to_numeric(df["grade"], errors="coerce")
    v = df[df["grade_int"].between(1, 4)].copy()

    for c in ["dev_mobile", "dev_media", "dev_compute", "dev_iot"]:
        v[c + "_n"] = v[c].apply(to_int_dev)
    for c in ["q_school", "q_home", "q_city", "q_equip"]:
        v[c + "_n"] = pd.to_numeric(v[c], errors="coerce")

    v["dev_total"] = v[["dev_mobile_n", "dev_media_n", "dev_compute_n", "dev_iot_n"]].sum(axis=1, min_count=1)
    v["DAE"] = minmax((zscore(v["q_home_n"]) + zscore(v["dev_total"])) / 2)
    v["SDR"] = minmax((zscore(v["q_school_n"]) + zscore(v["q_equip_n"])) / 2)

    sc_school_map = {
        "Áno, podrobne sme tento koncept preberali": 2,
        "Áno, ale len okrajovo": 1,
        "Nie som si istý/istá": 0,
        "Nepamätám sa": 0,
        "Nie, tento pojem som na strednej škole nezaznamenal/a": 0,
    }
    v["csa_school"] = v["sc_at_school"].map(sc_school_map)
    v["csa_role"] = (v["sc_role_tech"] ==
                     "Vylepšujú rôzne aspekty mestského života prostredníctvom dát a konektivity").astype(int)
    imp = {"Veľmi dôležité": 5, "Dôležité": 4, "Neutrálny názor": 3, "Málo dôležité": 2, "Nepodstatné": 1}
    v["csa_imp"] = v["sc_importance_edu"].map(imp)
    v["csa_local"] = (v["encountered_local"] == "Áno").astype(int)

    for c in ["csa_school", "csa_role", "csa_imp", "csa_local"]:
        v["Z_" + c] = zscore(v[c])
    v["CSA"] = minmax(v[["Z_csa_school", "Z_csa_role", "Z_csa_imp", "Z_csa_local"]].mean(axis=1))

    v["YSCR"] = (0.5 * v["CSA"]
                 + 0.3 * v["SDR"].fillna(v["SDR"].mean())
                 + 0.2 * v["DAE"].fillna(v["DAE"].mean()))

    out_cols = ["grade_int", "gender", "q_home_n", "q_school_n", "q_equip_n",
                "dev_total", "DAE", "SDR", "csa_school", "csa_role", "csa_imp",
                "csa_local", "CSA", "YSCR"]
    return v[out_cols].reset_index(drop=True)


if __name__ == "__main__":
    a = build_dataset_A()
    b = build_dataset_B()
    a.to_csv(DATA / "dataset_A_indices.csv", index=False)
    b.to_csv(DATA / "dataset_B_indices.csv", index=False)
    print(f"Dataset A: N = {len(a)}, AEI valid N = {a['AEI'].notna().sum()}")
    print(f"  AEI mean = {a['AEI'].mean():.2f}, SD = {a['AEI'].std():.2f}")
    print(f"Dataset B: N = {len(b)}, YSCR valid N = {b['YSCR'].notna().sum()}")
    print(f"  DAE mean = {b['DAE'].mean():.2f}, SDR = {b['SDR'].mean():.2f}, "
          f"CSA = {b['CSA'].mean():.2f}, YSCR = {b['YSCR'].mean():.2f}")
    print("Saved to data/dataset_A_indices.csv and data/dataset_B_indices.csv")
