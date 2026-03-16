#!/usr/bin/env python3
"""Generate report figures from detection and contrastive results.

Reads:
  outputs/detection/benchmark_summary.json
  outputs/contrastive/contrastive_summary.json

Generates:
  figures/detection_heatmap.png        — 6x5 heatmap of AUROC (detectors x representations)
  figures/detection_by_method.png      — bar chart of AUROC by detector (best representation)
  figures/contrastive_comparison.png   — bar chart: contrastive vs best classical detector
  figures/dr_improvement.png           — bar chart: raw vs best DR per detector
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DETECTION_DIR = ROOT / "outputs" / "detection"
CONTRASTIVE_DIR = ROOT / "outputs" / "contrastive"
FIGURES_DIR = ROOT / "figures"


def load_detection_results() -> list[dict]:
    path = DETECTION_DIR / "benchmark_summary.json"
    with open(path) as f:
        return json.load(f)


def load_contrastive_results() -> dict:
    path = CONTRASTIVE_DIR / "contrastive_summary.json"
    with open(path) as f:
        return json.load(f)


def build_auroc_matrix(results: list[dict]):
    """Build mean AUROC matrix: detectors (rows) x representations (cols)."""
    agg = defaultdict(list)
    for r in results:
        key = (r["detector"], r["representation"])
        if not np.isnan(r["auroc"]):
            agg[key].append(r["auroc"])

    detectors = sorted(set(r["detector"] for r in results))
    reps = sorted(set(r["representation"] for r in results))

    matrix = np.zeros((len(detectors), len(reps)))
    for i, det in enumerate(detectors):
        for j, rep in enumerate(reps):
            vals = agg.get((det, rep), [])
            matrix[i, j] = np.mean(vals) if vals else 0.0

    return matrix, detectors, reps


def fig1_detection_heatmap(results: list[dict]):
    """6x5 heatmap of AUROC (detectors x representations)."""
    matrix, detectors, reps = build_auroc_matrix(results)

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=0.4, vmax=1.0, aspect="auto")

    ax.set_xticks(range(len(reps)))
    ax.set_xticklabels([r.replace("_", "\n") for r in reps], fontsize=9)
    ax.set_yticks(range(len(detectors)))
    ax.set_yticklabels([d.replace("_", " ") for d in detectors], fontsize=9)

    # Annotate cells
    for i in range(len(detectors)):
        for j in range(len(reps)):
            color = "white" if matrix[i, j] < 0.6 else "black"
            ax.text(j, i, f"{matrix[i, j]:.3f}", ha="center", va="center",
                    fontsize=8, color=color, fontweight="bold")

    plt.colorbar(im, ax=ax, label="Mean AUROC (5 seeds)")
    ax.set_title("Detection AUROC: Detectors x Representations", fontsize=12, fontweight="bold")
    ax.set_xlabel("Representation")
    ax.set_ylabel("Detector")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "detection_heatmap.png", dpi=150)
    plt.close()
    print("  Saved detection_heatmap.png")


def fig2_detection_by_method(results: list[dict]):
    """Bar chart of AUROC by detector (best representation for each)."""
    agg = defaultdict(lambda: defaultdict(list))
    for r in results:
        if not np.isnan(r["auroc"]):
            agg[r["detector"]][r["representation"]].append(r["auroc"])

    detectors = sorted(agg.keys())
    best_aurocs = []
    best_reps = []
    std_aurocs = []

    for det in detectors:
        best_rep = max(agg[det].keys(), key=lambda rep: np.mean(agg[det][rep]))
        vals = agg[det][best_rep]
        best_aurocs.append(np.mean(vals))
        std_aurocs.append(np.std(vals))
        best_reps.append(best_rep)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(len(detectors)), best_aurocs, yerr=std_aurocs,
                  capsize=4, color=plt.cm.Set2(np.linspace(0, 1, len(detectors))),
                  edgecolor="black", linewidth=0.5)

    ax.set_xticks(range(len(detectors)))
    ax.set_xticklabels([f"{d.replace('_', ' ')}\n({r})" for d, r in zip(detectors, best_reps)],
                       fontsize=8)
    ax.set_ylabel("AUROC")
    ax.set_title("Best AUROC per Detector (best representation shown)", fontsize=12, fontweight="bold")
    ax.set_ylim(0.4, 1.05)
    ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5, label="Random baseline")
    ax.legend()

    # Annotate bars
    for bar, val in zip(bars, best_aurocs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.3f}", ha="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "detection_by_method.png", dpi=150)
    plt.close()
    print("  Saved detection_by_method.png")


def fig3_contrastive_comparison(results: list[dict], contrastive: dict):
    """Bar chart: contrastive vs best classical detector."""
    # Best classical detector (highest mean AUROC across all reps)
    agg = defaultdict(list)
    for r in results:
        if not np.isnan(r["auroc"]):
            agg[r["detector"]].append(r["auroc"])

    best_det = max(agg.keys(), key=lambda d: np.mean(agg[d]))
    classical_auroc = np.mean(agg[best_det])
    classical_std = np.std(agg[best_det])

    contrastive_auroc = contrastive["mean_auroc"]
    contrastive_std = contrastive["std_auroc"]

    fig, ax = plt.subplots(figsize=(6, 5))
    methods = [f"Best Classical\n({best_det.replace('_', ' ')})", "Contrastive\n(SimCLR-style)"]
    aurocs = [classical_auroc, contrastive_auroc]
    stds = [classical_std, contrastive_std]
    colors = ["#4ECDC4", "#FF6B6B"]

    bars = ax.bar(methods, aurocs, yerr=stds, capsize=5, color=colors,
                  edgecolor="black", linewidth=0.5, width=0.5)
    ax.set_ylabel("AUROC")
    ax.set_title("Contrastive vs Best Classical Detector", fontsize=12, fontweight="bold")
    ax.set_ylim(0.4, 1.1)
    ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5)

    for bar, val in zip(bars, aurocs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f"{val:.3f}", ha="center", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "contrastive_comparison.png", dpi=150)
    plt.close()
    print("  Saved contrastive_comparison.png")


def fig4_dr_improvement(results: list[dict]):
    """Bar chart: raw vs best DR per detector (side-by-side)."""
    agg = defaultdict(lambda: defaultdict(list))
    for r in results:
        if not np.isnan(r["auroc"]):
            agg[r["detector"]][r["representation"]].append(r["auroc"])

    detectors = sorted(agg.keys())
    raw_aurocs = []
    best_dr_aurocs = []
    best_dr_names = []

    for det in detectors:
        # Raw AUROC
        raw_vals = agg[det].get("raw", agg[det].get("raw_noDR", [0.5]))
        raw_aurocs.append(np.mean(raw_vals))

        # Best DR representation (exclude raw variants)
        dr_reps = {k: v for k, v in agg[det].items() if k not in ("raw", "raw_noDR")}
        if dr_reps:
            best_rep = max(dr_reps.keys(), key=lambda r: np.mean(dr_reps[r]))
            best_dr_aurocs.append(np.mean(dr_reps[best_rep]))
            best_dr_names.append(best_rep)
        else:
            best_dr_aurocs.append(raw_aurocs[-1])
            best_dr_names.append("none")

    x = np.arange(len(detectors))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    bars1 = ax.bar(x - width/2, raw_aurocs, width, label="Raw (512-dim)",
                   color="#95E1D3", edgecolor="black", linewidth=0.5)
    bars2 = ax.bar(x + width/2, best_dr_aurocs, width, label="Best DR (50-dim)",
                   color="#F38181", edgecolor="black", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{d.replace('_', ' ')}\n(best: {n})"
                        for d, n in zip(detectors, best_dr_names)], fontsize=7)
    ax.set_ylabel("AUROC")
    ax.set_title("Effect of Dimensionality Reduction on Detection", fontsize=12, fontweight="bold")
    ax.set_ylim(0.4, 1.1)
    ax.legend()
    ax.axhline(0.5, color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "dr_improvement.png", dpi=150)
    plt.close()
    print("  Saved dr_improvement.png")


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading detection results...")
    det_results = load_detection_results()
    print(f"  {len(det_results)} detection results loaded")

    print("Loading contrastive results...")
    contrastive = load_contrastive_results()
    print(f"  Contrastive mean AUROC: {contrastive['mean_auroc']}")

    print("\nGenerating figures...")
    fig1_detection_heatmap(det_results)
    fig2_detection_by_method(det_results)
    fig3_contrastive_comparison(det_results, contrastive)
    fig4_dr_improvement(det_results)

    print(f"\nAll figures saved to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
