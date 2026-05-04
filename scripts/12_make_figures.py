"""Generate PNG versions of Figure 1 (conceptual model) and Figure 2 (4 histograms)
using matplotlib so they can be embedded directly in the Word document.

Output (relative to repository root):
  results/Figure_1_conceptual_model.png
  results/Figure_2_index_histograms.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)


def figure_1():
    fig, ax = plt.subplots(figsize=(11.5, 7.5), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(x, y, w, h, text, sub=None, fill="#ffffff", edge="#1f2937", lw=1.2,
            text_color="#111827", sub_color="#4b5563", text_size=11, sub_size=9, bold=True):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.4,rounding_size=1.2",
            facecolor=fill, edgecolor=edge, linewidth=lw,
        ))
        ax.text(x + w / 2, y + h - 4 if sub else y + h / 2, text,
                ha="center", va="center", fontsize=text_size,
                fontweight="bold" if bold else "normal", color=text_color)
        if sub:
            ax.text(x + w / 2, y + 3, sub, ha="center", va="center",
                    fontsize=sub_size, color=sub_color)

    def arrow(x1, y1, x2, y2, color="#1f2937", lw=1.4, soft=False):
        style = "-|>"
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
            color=color, lw=lw, linestyle="--" if soft else "-",
        ))

    # Title
    ax.text(50, 96, "Figure 1 — Conceptual model: from app use to Youth Smart-City Readiness",
            ha="center", va="center", fontsize=14, fontweight="bold", color="#111827")

    # Inputs (left)
    ax.text(13, 88, "Inputs", fontsize=11, fontweight="bold", color="#111827")
    box(2, 75, 24, 10, "Uses & Gratifications",
        sub="motives: information, social,\nentertainment, school, trends",
        fill="#f3f4f6", text_size=10, sub_size=8)
    box(2, 60, 24, 10, "Socio-technical context",
        sub="recommender systems, peer signals,\nads, household & school setting",
        fill="#f3f4f6", text_size=10, sub_size=8)

    # Practice layer (centre, blue)
    ax.text(48, 73, "Practice layer", fontsize=10, fontweight="bold", color="#111827", ha="center")
    box(33, 60, 30, 10, "App Engagement Index (AEI)",
        sub="time in apps · installed apps · adoption recency",
        fill="#dbeafe", edge="#1e40af", text_color="#1e3a8a", sub_color="#1e3a8a",
        text_size=11, sub_size=8)

    # Infrastructure layer (green, two boxes)
    ax.text(50, 46, "Infrastructure layer", fontsize=10, fontweight="bold", color="#111827", ha="center")
    box(20, 33, 30, 10, "DAE — Digital Access Environment",
        sub="home internet · devices per household",
        fill="#dcfce7", edge="#166534", text_color="#14532d", sub_color="#14532d",
        text_size=10, sub_size=8)
    box(53, 33, 30, 10, "SDR — School Digital Readiness",
        sub="school internet · classroom equipment",
        fill="#dcfce7", edge="#166534", text_color="#14532d", sub_color="#14532d",
        text_size=10, sub_size=8)

    # Civic-literacy layer (yellow)
    ax.text(50, 20, "Civic-literacy layer", fontsize=10, fontweight="bold", color="#111827", ha="center")
    box(33, 6, 30, 12, "CSA — Curricular & Smart-City Awareness",
        sub="school exposure · concept understanding ·\nperceived importance · local feature recognition",
        fill="#fef3c7", edge="#a16207", text_color="#713f12", sub_color="#713f12",
        text_size=10, sub_size=8)

    # Composite YSCR (top, red)
    ax.add_patch(FancyBboxPatch(
        (28, 86), 44, 8,
        boxstyle="round,pad=0.5,rounding_size=2",
        facecolor="#fee2e2", edgecolor="#7f1d1d", linewidth=2,
    ))
    ax.text(50, 92, "YSCR — Youth Smart-City Readiness",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#7f1d1d")
    ax.text(50, 88.6, "composite: 0.5·CSA + 0.3·SDR + 0.2·DAE  (0–100)",
            ha="center", va="center", fontsize=8.5, color="#7f1d1d")

    # Arrows: inputs → AEI
    arrow(26, 80, 33, 67, color="#6b7280", lw=1, soft=True)
    arrow(26, 65, 33, 65, color="#6b7280", lw=1, soft=True)
    # AEI → YSCR
    arrow(48, 70, 48, 86)
    # DAE → YSCR
    arrow(35, 43, 38, 86)
    # SDR → YSCR
    arrow(68, 43, 60, 86)
    # CSA → YSCR
    arrow(48, 18, 50, 86)

    fig.text(0.5, 0.04,
             "Source: authors' own elaboration. Anchored in U&G (Katz, Blumler & Gurevitch 1973), "
             "DigComp 2.2 (Vuorikari, Kluzer & Punie 2022), DLGF (UNESCO 2018) and the Smart-City literature "
             "(Giffinger et al. 2007; Caragliu et al. 2011).",
             ha="center", fontsize=8, color="#4b5563", wrap=True)

    plt.savefig(OUT / "Figure_1_conceptual_model.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("Figure 1 PNG saved")


def figure_2():
    # Real data from the replication script (mainstream grades 1-4 sample)
    bins = np.arange(0, 110, 10)
    panels = [
        {
            "title": "DAE — Digital Access Environment",
            "meta": "N = 342  ·  M = 38.58  ·  SD = 13.91",
            "counts": [4, 29, 53, 99, 103, 40, 6, 4, 3, 1],
            "mean": 38.58, "color": "#2563eb", "edge": "#1e3a8a",
        },
        {
            "title": "SDR — School Digital Readiness",
            "meta": "N = 354  ·  M = 45.65  ·  SD = 25.06",
            "counts": [13, 46, 51, 69, 5, 51, 51, 32, 26, 10],
            "mean": 45.65, "color": "#16a34a", "edge": "#14532d",
        },
        {
            "title": "CSA — Curricular & Smart-City Awareness",
            "meta": "N = 368  ·  M = 67.93  ·  SD = 14.51",
            "counts": [2, 1, 1, 8, 10, 71, 101, 104, 55, 15],
            "mean": 67.93, "color": "#d97706", "edge": "#713f12",
        },
        {
            "title": "YSCR — Youth Smart-City Readiness",
            "meta": "N = 368  ·  M = 55.38  ·  SD = 11.74  (default weights)",
            "counts": [0, 0, 5, 29, 80, 128, 92, 24, 9, 1],
            "mean": 55.38, "color": "#b91c1c", "edge": "#7f1d1d",
        },
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0), dpi=200)
    axes = axes.flatten()
    for ax, p in zip(axes, panels):
        centers = (bins[:-1] + bins[1:]) / 2
        ax.bar(centers, p["counts"], width=9, color=p["color"], edgecolor=p["edge"],
               linewidth=0.7, alpha=0.95)
        ax.axvline(p["mean"], color="#111827", linestyle="--", linewidth=1.4)
        ax.text(p["mean"] + 1.2, max(p["counts"]) * 0.92, f"M = {p['mean']:.1f}",
                fontsize=9, color="#111827", fontweight="semibold")
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Index score (0–100)", fontsize=9.5, color="#1f2937")
        ax.set_ylabel("Frequency", fontsize=9.5, color="#1f2937")
        ax.set_title(p["title"], fontsize=11.5, fontweight="bold", color="#111827", pad=8)
        ax.text(0.5, 1.03, p["meta"], transform=ax.transAxes, ha="center",
                fontsize=9, color="#4b5563")
        ax.tick_params(labelsize=8.5, colors="#374151")
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#1f2937")
        ax.spines["bottom"].set_color("#1f2937")
        ax.grid(axis="y", color="#e5e7eb", linewidth=0.6)
    fig.suptitle("Figure 2 — Distribution of DAE, SDR, CSA and YSCR (Dataset B)",
                 fontsize=14, fontweight="bold", color="#111827", y=0.99)
    fig.text(0.5, 0.005,
             "Source: authors' own elaboration based on Dataset B (Slovak secondary-school students, 2025; "
             "mainstream grades 1–4). Bin width = 10 points. Dashed line = sample mean. "
             "Computed by scripts/01_build_indices.py in the public replication package.",
             ha="center", fontsize=8, color="#4b5563", wrap=True)
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(OUT / "Figure_2_index_histograms.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("Figure 2 PNG saved")


if __name__ == "__main__":
    figure_1()
    figure_2()
    for f in OUT.glob("Figure_*.png"):
        print(" ", f.name, f.stat().st_size, "B")
