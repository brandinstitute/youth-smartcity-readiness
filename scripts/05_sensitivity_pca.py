"""05_sensitivity_pca.py — YSCR sensitivity analysis: default vs equal vs PCA-derived."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)


def main() -> None:
    b = pd.read_csv(DATA / "dataset_B_indices.csv")
    sub = b[["DAE", "SDR", "CSA"]].dropna()
    Xz = StandardScaler().fit_transform(sub)
    pca = PCA(n_components=3).fit(Xz)
    w = np.abs(pca.components_[0])
    w = w / w.sum()

    print("PC1 explained variance:", round(pca.explained_variance_ratio_[0], 3))
    print(f"PCA-derived weights: DAE={w[0]:.3f}, SDR={w[1]:.3f}, CSA={w[2]:.3f}")

    b = b.copy()
    dae_mean = b["DAE"].mean(); sdr_mean = b["SDR"].mean()
    b["YSCR_default"] = 0.5 * b["CSA"] + 0.3 * b["SDR"].fillna(sdr_mean) + 0.2 * b["DAE"].fillna(dae_mean)
    b["YSCR_equal"] = (b["CSA"] + b["SDR"].fillna(sdr_mean) + b["DAE"].fillna(dae_mean)) / 3
    b["YSCR_pca"] = (w[0] * b["DAE"].fillna(dae_mean)
                     + w[1] * b["SDR"].fillna(sdr_mean)
                     + w[2] * b["CSA"])

    out = b[["YSCR_default", "YSCR_equal", "YSCR_pca"]].describe().round(2)
    out.to_csv(RES / "yscr_sensitivity_descriptives.csv")
    corr = b[["YSCR_default", "YSCR_equal", "YSCR_pca"]].corr().round(3)
    corr.to_csv(RES / "yscr_sensitivity_correlations.csv")

    print("\nDescriptives across YSCR variants:")
    print(out)
    print("\nPearson correlations across variants:")
    print(corr)


if __name__ == "__main__":
    main()
