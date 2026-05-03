"""04_clusters.py — k-means clustering (k = 2..6) on Dataset A behavioural features."""
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score

DATA = Path(__file__).resolve().parents[1] / "data"
RES = Path(__file__).resolve().parents[1] / "results"
RES.mkdir(exist_ok=True)


def main() -> None:
    a = pd.read_csv(DATA / "dataset_A_indices.csv")
    feats = ["AEI", "motives_count", "m_entertain", "m_school", "m_trend", "m_curiosity"]
    sub = a[feats].dropna()
    X = StandardScaler().fit_transform(sub)

    rows = []
    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=42, n_init=20).fit(X)
        rows.append({"k": k,
                     "silhouette": round(silhouette_score(X, km.labels_), 3),
                     "CH": round(calinski_harabasz_score(X, km.labels_), 2)})
    pd.DataFrame(rows).to_csv(RES / "cluster_diagnostics.csv", index=False)

    km4 = KMeans(n_clusters=4, random_state=42, n_init=20).fit(X)
    sub = sub.copy()
    sub["cluster"] = km4.labels_
    profiles = sub.groupby("cluster").mean().round(2)
    profiles["N"] = sub.groupby("cluster").size()
    profiles["pct"] = (100 * profiles["N"] / len(sub)).round(1)
    profiles.to_csv(RES / "cluster_profiles_k4.csv")

    print("Cluster diagnostics:")
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nk=4 cluster profiles:")
    print(profiles.to_string())


if __name__ == "__main__":
    main()
