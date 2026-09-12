#!/usr/bin/env python3
"""
Evaluation Protocol Outweighs Multimodal Fusion in Wearable Stress and Attention
Monitoring: Systematic Review and Meta-Analysis

Single self-contained generator for EVERY figure in the manuscript.

  Figure 1  system block diagram          -> emits fig1_block.tex   (LaTeX / TikZ)
  Figure 2  PRISMA flow diagram           -> emits fig2_prisma.tex  (LaTeX / TikZ)
  Figures 3-10  data figures              -> renders PNG via matplotlib

Figures 1 and 2 are authored in TikZ because the manuscript requires block and
PRISMA diagrams to be drawn natively in LaTeX; this script writes their complete
source so that all figure code lives in one place.

Usage
-----
    python3 make_all_figures.py [--outdir ../figures] [--texdir .]

Requires: matplotlib, numpy.  No other project file is needed; every datum used
by every figure is embedded below and is traceable to the reference number given
in the `ref` field.

Author: manuscript build pipeline
"""

import argparse
import os
import re
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedFormatter, FixedLocator, MaxNLocator, NullFormatter

# =============================================================================
# 1. EVIDENCE BASE
#    Every value was independently corroborated against the publisher or indexed
#    record. `ref` is the reference number in the manuscript bibliography.
# =============================================================================

# --- 1a. Corroborated headline outcomes --------------------------------------
OUTCOMES = [
    dict(ref=26,  study="Awada et al.",          year=2024, mod="EDA+BVP+TEMP+behav.",  n=None,
         dataset="In-house (office)",       protocol="NR",                  metric="Accuracy", value=82.78, classes=4),
    dict(ref=37,  study="Kim et al.",            year=2024, mod="EEG+GSR",              n=30,
         dataset="In-house (VR interview)", protocol="NR",                  metric="AUROC",    value=95.40, classes=2),
    dict(ref=12,  study="Campanella et al.",     year=2023, mod="PPG+EDA",              n=29,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=90.00, classes=2),
    dict(ref=33,  study="Li & Washington",       year=2024, mod="BVP+EDA+TEMP",         n=15,
         dataset="WESAD",                   protocol="Personalized",        metric="Accuracy", value=95.06, classes=3),
    dict(ref=33,  study="Li & Washington",       year=2024, mod="BVP+EDA+TEMP",         n=15,
         dataset="WESAD",                   protocol="Subject-independent", metric="Accuracy", value=67.65, classes=3),
    dict(ref=58,  study="Rashid et al.",         year=2023, mod="BVP+EDA+TEMP+ACC",     n=15,
         dataset="WESAD",                   protocol="NR",                  metric="Accuracy", value=94.12, classes=2),
    dict(ref=58,  study="Rashid et al.",         year=2023, mod="BVP+EDA+TEMP+ACC",     n=15,
         dataset="WESAD",                   protocol="NR",                  metric="Accuracy", value=86.34, classes=3),
    dict(ref=43,  study="Barki et al.",          year=2025, mod="In-ear PPG",           n=15,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=97.78, classes=2),
    dict(ref=50,  study="Ali et al. (ReTeNet)",  year=2025, mod="BVP",                  n=15,
         dataset="WESAD",                   protocol="NR",                  metric="Accuracy", value=98.23, classes=3),
    dict(ref=47,  study="Ali et al. (SADDNet)",  year=2026, mod="PPG",                  n=50,
         dataset="CATSA+WESAD",             protocol="LOSO",                metric="Accuracy", value=92.25, classes=2),
    dict(ref=55,  study="Ali et al. (TEANet)",   year=2026, mod="BVP",                  n=15,
         dataset="WESAD",                   protocol="LOSO",                metric="Accuracy", value=96.94, classes=2),
    dict(ref=55,  study="Ali et al. (TEANet)",   year=2026, mod="BVP",                  n=19,
         dataset="RUET-SPML",               protocol="LOSO",                metric="Accuracy", value=92.94, classes=2),
    dict(ref=61,  study="Khayyat et al.",        year=2024, mod="HRV",                  n=15,
         dataset="WESAD",                   protocol="NR",                  metric="Accuracy", value=96.76, classes=3),
    dict(ref=61,  study="Khayyat et al.",        year=2024, mod="HRV",                  n=25,
         dataset="SWELL-KW",                protocol="NR",                  metric="Accuracy", value=92.76, classes=3),
    dict(ref=54,  study="Momeni et al.",         year=2022, mod="ECG+EDA+RESP+TEMP",    n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=90.98, classes=2),
    dict(ref=16,  study="Xu et al.",             year=2024, mod="Facial video (rPPG)",  n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=94.33, classes=2),
    dict(ref=16,  study="Xu et al.",             year=2024, mod="Facial video (rPPG)",  n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=83.83, classes=3),
    dict(ref=99,  study="Gedam et al.",          year=2025, mod="ECG+GSR+TEMP",         n=200,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=96.17, classes=2),
    dict(ref=19,  study="Hongn et al.",          year=2025, mod="EDA+BVP+TEMP+ACC",     n=36,
         dataset="In-house (public)",       protocol="NR",                  metric="Accuracy", value=93.00, classes=2),
    dict(ref=30,  study="Fernandez et al.",      year=2025, mod="EEG",                  n=None,
         dataset="In-house",                protocol="Subject-independent", metric="Accuracy", value=86.24, classes=3),
    dict(ref=4,   study="Rescio et al.",         year=2024, mod="EEG+ECG+EDA",          n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=95.38, classes=2),
    dict(ref=74,  study="Chen & Lee",            year=2023, mod="ECG",                  n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=93.42, classes=2),
    dict(ref=75,  study="Abdul Kader et al.",    year=2024, mod="EEG+GSR",              n=20,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=84.60, classes=2),
    dict(ref=13,  study="Toshnazarov et al.",    year=2024, mod="PPG+ACC+context",      n=26,
         dataset="In-house (lab)",          protocol="NR",                  metric="F1",       value=84.00, classes=2),
    dict(ref=13,  study="Toshnazarov et al.",    year=2024, mod="PPG+ACC+context",      n=18,
         dataset="In-house (field)",        protocol="NR",                  metric="F1",       value=71.00, classes=2),
    dict(ref=1,   study="Alsahreef et al.",      year=2026, mod="HRV",                  n=None,
         dataset="PARFAIT",                 protocol="NR",                  metric="Accuracy", value=98.10, classes=2),
    dict(ref=5,   study="Donati et al.",         year=2023, mod="ECG",                  n=None,
         dataset="In-house (factory)",      protocol="NR",                  metric="Accuracy", value=88.40, classes=2),
    dict(ref=14,  study="Mohammadi et al.",      year=2022, mod="ECG+EDA+RESP+TEMP",    n=15,
         dataset="WESAD",                   protocol="NR",                  metric="Accuracy", value=96.00, classes=2),
    dict(ref=21,  study="El Arwadi & Abu Daher", year=2025, mod="ECG (HRV)",            n=None,
         dataset="In-house",                protocol="LOSO",                metric="Accuracy", value=90.80, classes=2),
    dict(ref=25,  study="Kumar et al.",          year=2024, mod="PPG+EDA+TEMP",         n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=94.00, classes=2),
    dict(ref=49,  study="Laiti et al.",          year=2026, mod="PPG (HRV)",            n=15,
         dataset="WESAD",                   protocol="NR",                  metric="AUROC",    value=91.58, classes=2),
    dict(ref=49,  study="Laiti et al.",          year=2026, mod="PPG (HRV)",            n=None,
         dataset="Wellby (real world)",     protocol="NR",                  metric="AUROC",    value=77.02, classes=2),
    dict(ref=53,  study="Shikha et al.",         year=2024, mod="EDA+BVP+HRV",          n=None,
         dataset="In-house",                protocol="NR",                  metric="Accuracy", value=98.28, classes=2),
    dict(ref=109, study="Kim et al.",            year=2025, mod="HR+step count",        n=None,
         dataset="In-house (free living)",  protocol="NR",                  metric="Accuracy", value=74.40, classes=2),
]

# --- 1b. Within-study, protocol-matched unimodal -> multimodal contrasts ------
FUSION = [
    dict(ref=75, study="Abdul Kader et al. (2024)", uni="EEG",           multi="EEG+GSR",
         level="Feature-level",  metric="Accuracy", u=70.30, m=84.60, n=20),
    dict(ref=12, study="Campanella et al. (2023)",  uni="PPG (HR)",      multi="PPG+EDA",
         level="Feature-level",  metric="Accuracy", u=83.89, m=90.00, n=29),
    dict(ref=26, study="Awada et al. (2024)",       uni="Physiological", multi="Physiological + behavioral",
         level="Decision-level", metric="Accuracy", u=79.55, m=82.78, n=None),
    dict(ref=37, study="Kim et al. (2024)",         uni="GSR",           multi="EEG+GSR",
         level="Feature-level",  metric="AUROC",    u=94.40, m=95.40, n=30),
]

# --- 1c. Within-study contrasts attributable to evaluation choices -----------
PROTOCOL = [
    dict(ref=33, study="Li & Washington (2024)",  contrast="Personalized vs subject-independent",
         kind="Personalization",    metric="Accuracy", hi=95.06, lo=67.65),
    dict(ref=33, study="Li & Washington (2024)",  contrast="Personalized vs subject-independent",
         kind="Personalization",    metric="F1",       hi=91.71, lo=43.05),
    dict(ref=13, study="Toshnazarov et al. (2024)", contrast="Laboratory vs free-living",
         kind="Deployment setting", metric="F1",       hi=84.00, lo=71.00),
    dict(ref=55, study="Ali et al. (2026, TEANet)", contrast="WESAD vs in-house cohort",
         kind="Dataset transfer",   metric="Accuracy", hi=96.94, lo=92.94),
    dict(ref=61, study="Khayyat et al. (2024)",     contrast="WESAD vs SWELL-KW",
         kind="Dataset transfer",   metric="Accuracy", hi=96.76, lo=92.76),
    dict(ref=58, study="Rashid et al. (2023)",      contrast="Binary vs three-class",
         kind="Task granularity",   metric="Accuracy", hi=94.12, lo=86.34),
    dict(ref=16, study="Xu et al. (2024)",          contrast="Stress state vs stress level",
         kind="Task granularity",   metric="Accuracy", hi=94.33, lo=83.83),
    dict(ref=61, study="Khayyat et al. (2024)",     contrast="Binary vs multiclass (WESAD)",
         kind="Task granularity",   metric="Accuracy", hi=99.82, lo=96.76),
    dict(ref=49, study="Laiti et al. (2026)",       contrast="WESAD vs Wellby real-world cohort",
         kind="Dataset transfer",   metric="AUROC",    hi=91.58, lo=77.02),
    dict(ref=53, study="Shikha et al. (2024)",      contrast="Two-level vs three-level stress",
         kind="Task granularity",   metric="Accuracy", hi=98.28, lo=97.02),
]

# --- 1d. Screened corpus (derived from the 116 screened bibliographic records) -
YEARS = ["2022", "2023", "2024", "2025", "2026"]
AREAS = ["Laboratory", "Benchmark", "Daily life", "Occupational",
         "Clinical", "Education", "Driving", "Aviation"]
YEAR_AREA = {                       # included studies per area per year
    "Laboratory":   [3, 1, 4, 9, 2],
    "Benchmark":    [1, 4, 3, 1, 3],
    "Daily life":   [1, 3, 2, 1, 2],
    "Occupational": [0, 2, 3, 0, 1],
    "Clinical":     [1, 2, 1, 1, 0],
    "Education":    [0, 1, 1, 2, 1],
    "Driving":      [0, 0, 0, 3, 0],
    "Aviation":     [0, 1, 0, 0, 0],
}
EXCLUSIONS = {"E3": 41, "E4": 10, "E2": 3, "E1": 2}
EXCL_LABEL = {
    "E3": "Outcome outside\nstress / attention scope",
    "E4": "No quantitative\nmodel evaluation",
    "E2": "Not a peer-reviewed\njournal article",
    "E1": "Outside the\n2022-2026 window",
}
PUBLISHERS = {"IEEE": 27, "MDPI": 10, "Elsevier": 8, "PLOS": 6,
              "Springer Nature": 4, "JMIR": 2, "Springer": 2, "BMC": 1}
N_INCLUDED, N_EXCLUDED = 60, 56

# --- 1e. Verification audit --------------------------------------------------
ATTEMPTED = list(range(60))          # corroboration attempted for all 60 included studies
CORROBORATED = [1, 4, 5, 12, 13, 14, 16, 19, 21, 25, 26, 30, 33, 37, 43, 47, 49,
                50, 53, 54, 55, 58, 61, 74, 75, 99, 101, 109]
RECOVER = {                          # reporting items recoverable from the public record
    "Headline metric":         28,
    "Evaluation cohort size":  18,
    "Public benchmark used":   14,
    "Validation protocol":      8,
    "Variance or CI reported":  3,
}

# =============================================================================
# 2. SHARED STYLE
# =============================================================================
# Figures are laid out so that, after being scaled to the 6.87 in text width of
# the manuscript, every label renders at roughly 10 pt against 11 pt body text.
# Two-panel figures are therefore stacked vertically: each panel then occupies
# the full text width instead of half of it.
FIGW = 10.0                      # canvas width (in) -> 0.687 scale on the page
plt.rcParams.update({
    "font.size": 15, "axes.titlesize": 16.5, "axes.labelsize": 15,
    "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 13.5,
    "figure.dpi": 200, "savefig.dpi": 400, "savefig.bbox": "tight",
    "axes.grid": True, "grid.alpha": 0.25, "grid.linestyle": ":",
    "axes.axisbelow": True, "font.family": "DejaVu Sans",
})

C = dict(blue="#2B6CB0", orange="#DD6B20", green="#2F855A", red="#C53030",
         purple="#6B46C1", teal="#2C7A7B", grey="#4A5568", gold="#B7791F",
         pink="#B83280", slate="#718096")
AREA_COLORS = [C["blue"], C["teal"], C["green"], C["orange"],
               C["red"], C["purple"], C["gold"], C["slate"]]
PROTO_COLOR = {"LOSO": C["green"], "Subject-independent": C["red"],
               "Personalized": C["purple"], "NR": C["slate"]}
KIND_COLOR = {"Personalization": C["purple"], "Deployment setting": C["red"],
              "Task granularity": C["orange"], "Dataset transfer": C["teal"]}
RNG = np.random.default_rng(7)


def label_panels(fig, axes):
    """Stamp (a), (b), ... at the left margin above each panel.

    Called after tight_layout so the axes positions are final; this keeps the
    letters clear of long tick labels and of the panel titles.
    """
    fig.canvas.draw()
    for ax, letter in zip(np.atleast_1d(axes), "abcdefgh"):
        bb = ax.get_position()
        fig.text(0.004, bb.y1 + 0.006, f"({letter})", fontsize=17,
                 fontweight="bold", va="bottom", ha="left")


def save(fig, outdir, name):
    path = os.path.join(outdir, name)
    fig.savefig(path)
    plt.close(fig)
    print("  wrote", path)


# =============================================================================
# 3. FIGURE 3  corpus composition
# =============================================================================
def figure3(outdir):
    M = np.array([YEAR_AREA[a] for a in AREAS], float)
    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 7.6))

    bot = np.zeros(len(YEARS))
    for i, a in enumerate(AREAS):
        ax[0].bar(YEARS, M[i], bottom=bot, label=a, color=AREA_COLORS[i],
                  edgecolor="white", linewidth=1.1, width=0.66)
        bot += M[i]
    for x, t in enumerate(bot):
        ax[0].text(x, t + 0.4, f"{int(t)}", ha="center", fontweight="bold", fontsize=15)
    ax[0].set_xlabel("Publication year")
    ax[0].set_ylabel("Included studies")
    ax[0].set_title("Included studies by year and application area")
    ax[0].set_ylim(0, bot.max() + 9.5)
    ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    ax[0].legend(ncol=4, frameon=False, loc="upper left", fontsize=13,
                 columnspacing=1.2, handlelength=1.4)

    tot = M.sum(1)
    order = np.argsort(tot)
    ax[1].barh([AREAS[i] for i in order], tot[order], height=0.66,
               color=[AREA_COLORS[i] for i in order], edgecolor="white", linewidth=1.1)
    for i, v in enumerate(tot[order]):
        ax[1].text(v + 0.25, i, f"{int(v)} ({v / tot.sum() * 100:.0f}%)",
                   va="center", fontsize=14)
    ax[1].set_xlabel("Included studies")
    ax[1].set_title("Application area of the included corpus")
    ax[1].set_xlim(0, tot.max() * 1.28)
    ax[1].grid(axis="y", alpha=0)

    fig.tight_layout(h_pad=2.6)
    label_panels(fig, ax)
    save(fig, outdir, "fig3_corpus.png")


# =============================================================================
# 4. FIGURE 4  screening outcome and provenance
#    FIX: exclusion-reason labels no longer collide; annotations use single
#    spacing; long publisher names are wrapped rather than rotated into overlap.
# =============================================================================
def figure4(outdir):
    keys = ["E3", "E4", "E2", "E1"]
    vals = [EXCLUSIONS[k] for k in keys]
    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 7.6))

    xs = np.arange(len(keys))
    ax[0].bar(xs, vals, width=0.58,
              color=[C["red"], C["orange"], C["gold"], C["slate"]],
              edgecolor="white", linewidth=1.1)
    for i, v in enumerate(vals):
        ax[0].text(i, v + 1.0, f"{v} ({v / N_EXCLUDED * 100:.0f}%)",
                   ha="center", fontweight="bold", fontsize=14.5)
    ax[0].set_xticks(xs)
    ax[0].set_xticklabels([EXCL_LABEL[k] for k in keys], fontsize=13.5, linespacing=1.4)
    ax[0].set_xlim(-0.6, len(keys) - 0.4)
    ax[0].set_ylabel("Records excluded")
    ax[0].set_ylim(0, max(vals) + 8)
    ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    ax[0].set_title(f"Reasons for exclusion at full-record appraisal (n = {N_EXCLUDED})")

    pk = list(PUBLISHERS)
    pv = [PUBLISHERS[p] for p in pk]
    ax[1].bar(np.arange(len(pk)), pv, width=0.58, color=C["blue"],
              edgecolor="white", linewidth=1.1)
    for i, v in enumerate(pv):
        ax[1].text(i, v + 0.5, str(v), ha="center", fontweight="bold", fontsize=14.5)
    ax[1].set_xticks(np.arange(len(pk)))
    ax[1].set_xticklabels([p.replace(" ", "\n") for p in pk], fontsize=13.5, linespacing=1.4)
    ax[1].set_ylabel("Included studies")
    ax[1].set_ylim(0, max(pv) + 4)
    ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
    ax[1].set_title(f"Publisher of record for the included corpus (n = {N_INCLUDED})")

    fig.tight_layout(h_pad=2.6)
    label_panels(fig, ax)
    save(fig, outdir, "fig4_screening.png")


# =============================================================================
# 5. FIGURE 5  accuracy by sensing configuration
# =============================================================================
def _family(mod):
    m = mod.lower()
    if "facial" in m:
        return "Camera (rPPG /\nfacial video)"
    if "eeg" in m and "+" in m:
        return "EEG + peripheral"
    if "eeg" in m:
        return "EEG only"
    if m.count("+") >= 2:
        return "Three or more\nchannels"
    if "+" in m:
        return "Two channels"
    return "Single PPG / BVP\nor ECG"


def figure5(outdir):
    acc = [o for o in OUTCOMES if o["metric"] == "Accuracy"]
    groups = {}
    for o in acc:
        groups.setdefault(_family(o["mod"]), []).append(o["value"])
    keys = sorted(groups, key=lambda k: -st.median(groups[k]))

    fig, ax = plt.subplots(figsize=(FIGW, 5.6))
    pos = np.arange(len(keys))
    bp = ax.boxplot([groups[k] for k in keys], positions=pos, widths=0.5,
                    patch_artist=True, medianprops=dict(color="black", lw=2.4),
                    whiskerprops=dict(lw=1.5), capprops=dict(lw=1.5),
                    flierprops=dict(marker=""))
    fills = [C["blue"], C["teal"], C["green"], C["orange"], C["purple"], C["red"]]
    for p, col in zip(bp["boxes"], fills):
        p.set_facecolor(col); p.set_alpha(0.32)
        p.set_edgecolor(col); p.set_linewidth(2)
    for i, k in enumerate(keys):
        v = groups[k]
        ax.scatter(np.full(len(v), i) + RNG.uniform(-0.15, 0.15, len(v)), v,
                   s=80, color=C["grey"], zorder=4, edgecolor="white", linewidth=1.1)
        ax.text(i, 102.2, f"k = {len(v)}", ha="center", fontsize=13.5, fontweight="bold")
        ax.text(i, 58.6, f"median\n{st.median(v):.1f}%", ha="center",
                fontsize=13, color=C["grey"])
    ax.set_xticks(pos)
    ax.set_xticklabels(keys, fontsize=13, linespacing=1.4)
    ax.set_ylabel("Corroborated accuracy (%)")
    ax.set_ylim(55, 106)
    ax.set_title("Corroborated classification accuracy by sensing configuration")
    ax.axhline(90, color=C["red"], ls="--", lw=1.8, alpha=0.8)
    ax.text(len(keys) - 0.45, 90.7, "90% reference", color=C["red"],
            fontsize=13, ha="right")
    fig.tight_layout()
    save(fig, outdir, "fig5_modality.png")


# =============================================================================
# 6. FIGURE 6  WESAD benchmark saturation
# =============================================================================
def figure6(outdir):
    w = [o for o in OUTCOMES if "WESAD" in o["dataset"]]
    def _name(o):
        base = o["study"].split(" et al")[0].split(" &")[0]
        m = re.search(r"\(([^)]+)\)", o["study"])
        return f"{base} {m.group(1)}" if m else base
    lab = [f"{_name(o)} {o['year']} ({o['classes']}-cls)" for o in w]
    val = [o["value"] for o in w]
    prot = [o["protocol"] for o in w]
    idx = np.argsort(val)

    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 8.4),
                           gridspec_kw={"height_ratios": [1.25, 1]})
    ax[0].barh(range(len(idx)), [val[i] for i in idx], height=0.66,
               color=[PROTO_COLOR[prot[i]] for i in idx],
               edgecolor="white", linewidth=1.2)
    ax[0].set_yticks(range(len(idx)))
    ax[0].set_yticklabels([lab[i] for i in idx], fontsize=13.5)
    for j, i in enumerate(idx):
        ax[0].text(val[i] + 0.6, j, f"{val[i]:.2f}", va="center",
                   fontsize=13.5, fontweight="bold")
    ax[0].set_xlim(60, 108)
    ax[0].set_xlabel("Reported accuracy on WESAD (%)")
    ax[0].set_title("WESAD results, ordered by reported accuracy")
    ax[0].grid(axis="y", alpha=0)
    order = ["Personalized", "NR", "LOSO", "Subject-independent"]
    handles = [plt.Rectangle((0, 0), 1, 1, color=PROTO_COLOR[k]) for k in order]
    ax[0].legend(handles, ["Personalized (subject-dependent)", "Protocol not reported",
                           "Leave-one-subject-out", "Subject-independent generalized"],
                 loc="upper center", bbox_to_anchor=(0.5, -0.19), ncol=2,
                 frameon=False, fontsize=12.5)

    byp = {}
    for v, p in zip(val, prot):
        byp.setdefault(p, []).append(v)
    ordk = [k for k in order if k in byp]
    for i, k in enumerate(ordk):
        v = byp[k]
        ax[1].scatter(np.full(len(v), i) + RNG.uniform(-0.08, 0.08, len(v)), v,
                      s=170, color=PROTO_COLOR[k], edgecolor="white",
                      linewidth=1.5, zorder=3)
        ax[1].hlines(st.median(v), i - 0.24, i + 0.24, color="black", lw=3, zorder=4)
        ax[1].text(i, 58.4, f"k = {len(v)}\nmedian {st.median(v):.1f}%",
                   ha="center", fontsize=12.5, linespacing=1.35)
    ax[1].set_xticks(range(len(ordk)))
    ax[1].set_xticklabels(["Personalized", "Not reported", "LOSO",
                           "Subject-independent"], fontsize=13.5)
    ax[1].set_xlim(-0.5, len(ordk) - 0.5)
    ax[1].set_ylabel("Accuracy on WESAD (%)")
    ax[1].set_ylim(53, 104)
    ax[1].set_title("The same benchmark, stratified by evaluation protocol")
    ax[1].axhspan(92, 100, color=C["gold"], alpha=0.13)
    ax[1].text(len(ordk) - 0.56, 101.2, "saturation band (92 to 100%)", fontsize=12.5,
               color=C["gold"], ha="right", va="center", fontweight="bold")

    fig.tight_layout(h_pad=4.6)
    label_panels(fig, ax)
    save(fig, outdir, "fig6_wesad.png")


# =============================================================================
# 7. FIGURE 7  within-study fusion gain
# =============================================================================
def figure7(outdir):
    fs = sorted(FUSION, key=lambda r: r["m"] - r["u"])
    lc = {"Feature-level": C["blue"], "Decision-level": C["orange"]}
    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 7.9))

    for i, r in enumerate(fs):
        col = lc[r["level"]]
        ax[0].plot([0, 1], [r["u"], r["m"]], "-o", color=col, lw=3, ms=12,
                   markeredgecolor="white", markeredgewidth=1.6, zorder=3)
        dy = {2: 1.0, 1: -1.0}.get(i, 0.0)
        ax[0].annotate(f"{r['study'].split(' (')[0]}  +{r['m'] - r['u']:.2f} pp",
                       (1.03, r["m"] + dy), fontsize=13.5, va="center",
                       color=col, fontweight="bold")
    ax[0].set_xlim(-0.14, 2.05)
    ax[0].set_xticks([0, 1])
    ax[0].set_xticklabels(["Best single modality", "Multimodal fusion"], fontsize=14.5)
    ax[0].set_ylabel("Reported performance (%)")
    ax[0].set_title("Within-study, protocol-matched fusion contrasts")
    handles = [plt.Line2D([], [], color=lc[k], lw=3, marker="o", ms=9) for k in lc]
    ax[0].legend(handles, list(lc), frameon=False, loc="lower left", fontsize=13)

    g = [r["m"] - r["u"] for r in fs]
    ax[1].barh(range(len(g)), g, height=0.6, color=[lc[r["level"]] for r in fs],
               edgecolor="white", linewidth=1.2)
    for i, v in enumerate(g):
        ax[1].text(v + 0.25, i, f"+{v:.2f} pp", va="center",
                   fontweight="bold", fontsize=14)
    ax[1].set_yticks(range(len(g)))
    ax[1].set_yticklabels([r["study"].split(" (")[0] for r in fs], fontsize=13.5)
    ax[1].axvline(st.median(g), color=C["red"], ls="--", lw=2.2)
    ax[1].text(st.median(g) + 0.25, -0.66, f"median +{st.median(g):.2f} pp",
               color=C["red"], fontsize=13.5, fontweight="bold")
    ax[1].set_xlabel("Gain over the best single modality (percentage points)")
    ax[1].set_xlim(0, max(g) * 1.3)
    ax[1].set_ylim(-1.0, len(g) - 0.35)
    ax[1].set_title("Magnitude of the corroborated fusion gain")
    ax[1].grid(axis="y", alpha=0)

    fig.tight_layout(h_pad=2.8)
    label_panels(fig, ax)
    save(fig, outdir, "fig7_fusion.png")


# =============================================================================
# 8. FIGURE 8  evaluation effects against fusion effects
#    FIX: the median-fusion-gain annotation is moved clear of the point cloud
#    into the empty upper-left region and joined to its line by a leader.
# =============================================================================
def figure8(outdir):
    kinds = ["Personalization", "Deployment setting", "Task granularity", "Dataset transfer"]
    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 10.2),
                           gridspec_kw={"height_ratios": [1.35, 1]})

    rows = sorted(PROTOCOL, key=lambda r: r["hi"] - r["lo"])
    for i, r in enumerate(rows):
        d = r["hi"] - r["lo"]
        col = KIND_COLOR[r["kind"]]
        ax[0].plot([r["lo"], r["hi"]], [i, i], color=col, lw=4.5, zorder=2)
        ax[0].scatter([r["lo"], r["hi"]], [i, i], s=130, color=col,
                      edgecolor="white", linewidth=1.5, zorder=3)
        ax[0].text(r["hi"] + 1.0, i, f"{d:.2f} pp", va="center",
                   fontsize=13.5, fontweight="bold", color=col)
    ax[0].set_yticks(range(len(rows)))
    _abbr = {"Personalized vs subject-independent": "Personalized vs subject-indep.",
             "WESAD vs Wellby real-world cohort": "WESAD vs real-world cohort"}
    ax[0].set_yticklabels(
        [f"{r['study'].split(' (')[0]}\n{_abbr.get(r['contrast'], r['contrast'])} "
         f"[{r['metric']}]" for r in rows], fontsize=12, linespacing=1.35)
    ax[0].set_xlabel("Reported performance (%)")
    ax[0].set_xlim(38, 116)
    ax[0].set_ylim(-1.1, len(rows) - 0.3)
    ax[0].set_title("Within-study contrasts attributable to evaluation choices")
    ax[0].grid(axis="y", alpha=0)
    handles = [plt.Line2D([], [], color=KIND_COLOR[k], lw=4.5) for k in kinds]
    ax[0].legend(handles, kinds, frameon=False, loc="upper center",
                 bbox_to_anchor=(0.5, -0.13), ncol=4, fontsize=12.5)

    fg = [r["m"] - r["u"] for r in FUSION]
    short = {"Personalization": "Personal-\nization", "Deployment setting": "Lab to\nfield",
             "Task granularity": "Task\ngranularity", "Dataset transfer": "Dataset\ntransfer"}
    cats, vals, cols = ["Fusion"], [fg], [C["blue"]]
    for k in kinds:
        cats.append(short[k])
        vals.append([r["hi"] - r["lo"] for r in PROTOCOL if r["kind"] == k])
        cols.append(KIND_COLOR[k])
    for i, (v, col) in enumerate(zip(vals, cols)):
        ax[1].scatter(np.full(len(v), i) + RNG.uniform(-0.07, 0.07, len(v)), v,
                      s=175, color=col, edgecolor="white", linewidth=1.6, zorder=3)
        ax[1].hlines(st.median(v), i - 0.26, i + 0.26, color="black", lw=3.2, zorder=4)
        ax[1].text(i, -7.0, f"k = {len(v)}\nmed {st.median(v):.1f}",
                   ha="center", fontsize=12.5, linespacing=1.35)
    med = st.median(fg)
    ax[1].axhline(med, color=C["blue"], ls="--", lw=2.2, alpha=0.85, zorder=1)
    ax[1].annotate(f"median fusion gain = {med:.2f} pp",
                   xy=(3.6, med), xytext=(1.55, 34),
                   fontsize=13.5, fontweight="bold", color=C["blue"], ha="left",
                   va="center",
                   bbox=dict(boxstyle="round,pad=0.35", fc="white",
                             ec=C["blue"], lw=1.4, alpha=0.96),
                   arrowprops=dict(arrowstyle="-", color=C["blue"], lw=1.4,
                                   shrinkA=2, shrinkB=2,
                                   connectionstyle="angle,angleA=0,angleB=90,rad=4"))
    ax[1].set_xticks(range(len(cats)))
    ax[1].set_xticklabels(cats, fontsize=13)
    ax[1].set_xlim(-0.55, len(cats) - 0.45)
    ax[1].set_ylabel("Within-study difference (pp)")
    ax[1].set_ylim(-11, 56)
    ax[1].set_title("Fusion gain against evaluation-induced differences")

    fig.tight_layout(h_pad=4.4)
    label_panels(fig, ax)
    save(fig, outdir, "fig8_protocol_vs_fusion.png")


# =============================================================================
# 9. FIGURE 9  transfer behavior and cohort size
#    FIX: the grouped-bar category labels are placed as a two-line legend-style
#    caption under each pair and no longer run into one another.
# =============================================================================
def figure9(outdir):
    tr = [r for r in PROTOCOL if r["kind"] in ("Deployment setting", "Dataset transfer")]
    short = {"Laboratory vs free-living": ("Toshnazarov et al.", "laboratory $\\rightarrow$", "free-living"),
             "WESAD vs in-house cohort":  ("Ali et al.", "WESAD $\\rightarrow$", "in-house cohort"),
             "WESAD vs SWELL-KW":         ("Khayyat et al.", "WESAD $\\rightarrow$", "SWELL-KW"),
             "WESAD vs Wellby real-world cohort": ("Laiti et al.", "WESAD $\\rightarrow$", "real world")}

    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 7.9))
    x = np.arange(len(tr))
    wd = 0.3
    ax[0].bar(x - wd / 2, [r["hi"] for r in tr], wd, label="Development condition",
              color=C["blue"], edgecolor="white", linewidth=1.2)
    ax[0].bar(x + wd / 2, [r["lo"] for r in tr], wd, label="Transfer condition",
              color=C["red"], edgecolor="white", linewidth=1.2)
    for i, r in enumerate(tr):
        ax[0].text(i - wd / 2, r["hi"] + 0.8, f"{r['hi']:.1f}", ha="center", fontsize=13.5)
        ax[0].text(i + wd / 2, r["lo"] + 0.8, f"{r['lo']:.1f}", ha="center", fontsize=13.5)
        ax[0].annotate(f"-{r['hi'] - r['lo']:.1f} pp", (i, max(r["hi"], r["lo"]) + 4.2),
                       ha="center", fontsize=14, fontweight="bold", color=C["red"])
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(["\n".join(short[r["contrast"]]) for r in tr],
                          fontsize=12.5, linespacing=1.5)
    ax[0].set_xlim(-0.55, len(tr) - 0.45)
    ax[0].set_ylabel("Reported performance (%)")
    ax[0].set_ylim(55, 112)
    ax[0].set_title("Loss on leaving the development condition")
    ax[0].legend(frameon=True, framealpha=0.95, loc="upper left", fontsize=13, ncol=2)

    sz = [(o["n"], o["value"], o["protocol"]) for o in OUTCOMES
          if o["n"] and o["metric"] == "Accuracy"]
    for n, v, p in sz:
        ax[1].scatter(n, v, s=170, color=PROTO_COLOR.get(p, C["slate"]),
                      edgecolor="white", linewidth=1.5, alpha=0.9, zorder=3)
    xs = np.array([s[0] for s in sz], float)
    ys = np.array([s[1] for s in sz])
    b, a = np.polyfit(np.log10(xs), ys, 1)
    gx = np.logspace(np.log10(xs.min()), np.log10(xs.max()), 60)
    ax[1].plot(gx, a + b * np.log10(gx), "--", color=C["grey"], lw=2.4)
    r = np.corrcoef(np.log10(xs), ys)[0, 1]
    ax[1].text(0.035, 0.07,
               f"slope = {b:+.1f} pp per decade,  Pearson r = {r:+.2f}  (k = {len(sz)})",
               transform=ax[1].transAxes, fontsize=13.5,
               bbox=dict(fc="white", ec=C["grey"], alpha=0.92))
    ax[1].set_xscale("log")
    ticks = [15, 20, 30, 50, 100, 200]
    ax[1].xaxis.set_major_locator(FixedLocator(ticks))
    ax[1].xaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))
    ax[1].xaxis.set_minor_formatter(NullFormatter())
    ax[1].set_xlabel("Participants in the evaluation cohort (log scale)")
    ax[1].set_ylabel("Corroborated accuracy (%)")
    ax[1].set_ylim(58, 104)
    ax[1].set_title("Reported accuracy against evaluation cohort size")

    fig.tight_layout(h_pad=2.8)
    label_panels(fig, ax)
    save(fig, outdir, "fig9_transfer.png")


# =============================================================================
# 10. FIGURE 10  verification and reporting audit
# =============================================================================
def figure10(outdir):
    na, nc = len(ATTEMPTED), len(CORROBORATED)
    fig, ax = plt.subplots(2, 1, figsize=(FIGW, 7.2))

    ax[0].bar(["Headline outcome corroborated", "Full text not openly retrievable"],
              [nc, na - nc], color=[C["green"], C["slate"]],
              edgecolor="white", linewidth=1.2, width=0.5)
    for i, v in enumerate([nc, na - nc]):
        ax[0].text(i, v + 0.6, f"{v} ({v / na * 100:.1f}%)", ha="center",
                   fontweight="bold", fontsize=14.5)
    ax[0].set_ylabel("Included studies")
    ax[0].set_ylim(0, na * 0.75)
    ax[0].set_xlim(-0.6, 1.6)
    ax[0].tick_params(axis="x", labelsize=13.5)
    ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    ax[0].set_title(f"Independent corroboration of reported outcomes (n = {na})")

    fields = list(RECOVER)
    ok = list(RECOVER.values())
    ax[1].barh(fields, [v / na * 100 for v in ok], height=0.6, color=C["blue"],
               edgecolor="white", linewidth=1.2)
    for i, v in enumerate(ok):
        ax[1].text(v / na * 100 + 1.2, i, f"{v}/{na} ({v / na * 100:.0f}%)",
                   va="center", fontsize=13.5, fontweight="bold")
    ax[1].set_xlabel("Studies for which the item was recoverable (%)")
    ax[1].set_xlim(0, 78)
    ax[1].grid(axis="y", alpha=0)
    ax[1].set_title("Recoverability of reporting items from the public record")
    ax[1].tick_params(axis="y", labelsize=13.5)

    fig.tight_layout(h_pad=2.6)
    label_panels(fig, ax)
    save(fig, outdir, "fig10_verifiability.png")

# =============================================================================
# 11. FIGURE 1  system block diagram  (LaTeX / TikZ source)
# =============================================================================
FIG1_TIKZ = r"""\begin{tikzpicture}[
  x=1mm, y=1mm,
  font=\sffamily,
  card/.style={rectangle, rounded corners=1.2mm, draw=#1, fill=#1!6,
               line width=0.55pt, align=center, inner sep=0pt},
  stage/.style={rectangle, rounded corners=1mm, fill=black!5, draw=none,
                inner sep=0pt, minimum width=17mm, align=center,
                font=\sffamily\bfseries\footnotesize, text=black!62},
  chip/.style={rectangle, rounded corners=0.9mm, draw=#1!70, fill=white,
               line width=0.45pt, inner xsep=1.7mm, inner ysep=1.0mm,
               font=\sffamily\footnotesize, text=#1!55!black},
  flow/.style={-{Straight Barb[length=1.5mm, width=1.5mm]},
               line width=0.8pt, draw=black!45},
  loop/.style={-{Straight Barb[length=1.5mm, width=1.5mm]},
               line width=0.7pt, draw=RED!75, dash pattern=on 1.4mm off 1.1mm},
  ttl/.style={font=\sffamily\bfseries\footnotesize, text=black!85},
  sub/.style={font=\sffamily\footnotesize, text=black!58},
]

\definecolor{GRN}{HTML}{2F7A4F}
\definecolor{PUR}{HTML}{7A4FA8}
\definecolor{ORG}{HTML}{C2701C}
\definecolor{BLU}{HTML}{2B6CB0}
\definecolor{RED}{HTML}{C03434}
\definecolor{TEA}{HTML}{2C7A7B}
\definecolor{GLD}{HTML}{A9761A}

%% ---------- geometry ----------
\def\SW{27}   % sensor card width
\def\SH{20}   % sensor card height
\def\GAP{2.6} % gap between sensor cards
\def\LX{-25}  % stage label column x

% mini waveform helper: #1 colour, #2 anchor node, #3 y-offset, #4 coords
\newcommand{\wave}[3]{\draw[line width=0.55pt, draw=#1, line cap=round] #2 #3;}

%% ================= STAGE 1 : ACQUISITION =================
\node[card=GRN, minimum width=\SW mm, minimum height=\SH mm] (s1) at (0,0) {};
\node[card=GRN, minimum width=\SW mm, minimum height=\SH mm] (s2) at (\SW+\GAP,0) {};
\node[card=GRN, minimum width=\SW mm, minimum height=\SH mm] (s3) at (2*\SW+2*\GAP,0) {};
\node[card=GRN, minimum width=\SW mm, minimum height=\SH mm] (s4) at (3*\SW+3*\GAP,0) {};
\node[card=GRN, minimum width=\SW mm, minimum height=\SH mm] (s5) at (4*\SW+4*\GAP,0) {};
\node[card=PUR, minimum width=\SW mm, minimum height=\SH mm] (s6)
      at (5*\SW+5*\GAP+7,0) {};

\foreach \n/\t/\l in {s1/{ECG / HRV}/{chest, patch},
                      s2/{PPG / BVP}/{wrist, in-ear},
                      s3/{EDA, skin temp.}/{wrist, finger},
                      s4/{EEG}/{scalp, behind-ear},
                      s5/{IMU}/{accel., gyro.},
                      s6/{RGB camera}/{face, gaze, pose}} {
  \node[ttl] at ([yshift=6.0mm]\n.center) {\t};
  \node[sub] at ([yshift=2.9mm]\n.center) {\l};
}

% --- signal glyphs ---
\begin{scope}[shift={([yshift=-3.6mm]s1.center)}]   % ECG
  \draw[line width=0.62pt, draw=GRN, line join=round]
    (-12,0) -- (-9.4,0) -- (-8.9,0.55) -- (-8.4,-0.9) -- (-8.05,3.3)
    -- (-7.7,-3.4) -- (-7.3,1.2) -- (-6.7,-0.25) -- (-4.6,0)
    -- (-2.0,0) -- (-1.5,0.55) -- (-1.0,-0.9) -- (-0.65,3.3)
    -- (-0.3,-3.4) -- (0.1,1.2) -- (0.7,-0.25) -- (2.8,0)
    -- (5.4,0) -- (5.9,0.55) -- (6.4,-0.9) -- (6.75,3.3)
    -- (7.1,-3.4) -- (7.5,1.2) -- (8.1,-0.25) -- (12,0);
\end{scope}
\begin{scope}[shift={([yshift=-3.6mm]s2.center)}]   % PPG
  \draw[line width=0.62pt, draw=GRN, smooth]
    plot[domain=-12:12, samples=110]
    (\x, {1.05*sin((\x+12)*45)^2 + 0.42*sin((\x+12)*90) - 0.9});
\end{scope}
\begin{scope}[shift={([yshift=-3.6mm]s3.center)}]   % EDA
  \draw[line width=0.62pt, draw=GRN, smooth]
    plot[domain=-12:12, samples=80]
    (\x, {-2.1 + 0.075*(\x+12) + 2.05*exp(-((\x-1)/3.4)^2)});
\end{scope}
\begin{scope}[shift={([yshift=-3.6mm]s4.center)}]   % EEG
  \draw[line width=0.55pt, draw=GRN, smooth]
    plot[domain=-12:12, samples=180]
    (\x, {0.95*sin(\x*152) + 0.62*sin(\x*63) + 0.34*sin(\x*311)});
\end{scope}
\begin{scope}[shift={([yshift=-3.6mm]s5.center)}]   % IMU
  \draw[line width=0.55pt, draw=GRN]
    (-12,1.3) -- (-8,1.3) -- (-8,2.5) -- (-4,2.5) -- (-4,0.9) -- (0.5,0.9)
    -- (0.5,2.1) -- (5,2.1) -- (5,1.3) -- (12,1.3);
  \draw[line width=0.55pt, draw=GRN!62]
    (-12,-1.0) -- (-6.5,-1.0) -- (-6.5,-2.3) -- (-1.5,-2.3) -- (-1.5,-0.3)
    -- (3.5,-0.3) -- (3.5,-1.6) -- (12,-1.6);
\end{scope}
\begin{scope}[shift={([yshift=-3.7mm]s6.center)}]   % camera: face + gaze cone
  \draw[line width=0.5pt, draw=PUR!55, dash pattern=on 0.7mm off 0.6mm]
        (-5.2,-3.9) rectangle (5.2,4.1);
  \draw[line width=0.62pt, draw=PUR] (-1.6,0) ellipse [x radius=2.9, y radius=3.5];
  \fill[PUR] (-2.65,0.95) circle (0.33);
  \fill[PUR] (-0.55,0.95) circle (0.33);
  \draw[line width=0.45pt, draw=PUR] (-2.7,-1.4) .. controls (-1.6,-2.4) .. (-0.5,-1.4);
  \draw[line width=0.4pt, draw=PUR!55] (-0.55,0.95) -- (4.6,2.5);
  \draw[line width=0.4pt, draw=PUR!55] (-0.55,0.95) -- (4.6,-0.6);
  \fill[PUR!14] (-0.55,0.95) -- (4.6,2.5) -- (4.6,-0.6) -- cycle;
\end{scope}

% group frames
\begin{scope}[on background layer]
  \node[draw=GRN!55, dash pattern=on 1.1mm off 0.9mm, rounded corners=1.5mm,
        line width=0.6pt, fill=GRN!3, fit=(s1)(s5), inner sep=2.4mm] (wgrp) {};
  \node[draw=PUR!55, dash pattern=on 1.1mm off 0.9mm, rounded corners=1.5mm,
        line width=0.6pt, fill=PUR!3, fit=(s6), inner sep=2.4mm] (vgrp) {};
\end{scope}
\node[font=\sffamily\bfseries\footnotesize, text=GRN, above=1.3mm of wgrp.north]
      {CONTACT SENSING: wearable physiological and inertial channels};
\node[font=\sffamily\bfseries\footnotesize, text=PUR, above=1.3mm of vgrp.north]
      {CONTACTLESS};

%% ================= STAGE 2 : CONDITIONING =================
\def\CW{91}
\node[card=ORG, minimum width=\CW mm, minimum height=16mm] (c1) at (32.2,-31) {};
\node[card=ORG, minimum width=78mm, minimum height=16mm] (c2) at (127,-31) {};
\node[ttl] at ([yshift=4.3mm]c1.center) {Signal conditioning};
\node[sub, align=center] at ([yshift=-1.3mm]c1.center)
      {band-pass filtering \ \textbullet\ \ motion-artifact rejection\\
       resampling \ \textbullet\ \ signal-quality gating};
\node[ttl] at ([yshift=4.3mm]c2.center) {Vision front end};
\node[sub, align=center] at ([yshift=-1.3mm]c2.center)
      {face detection \ \textbullet\ \ facial landmarks\\
       action units \ \textbullet\ \ gaze \ \textbullet\ \ rPPG extraction};

%% ================= STAGE 3 : REPRESENTATION =================
\node[card=ORG, minimum width=\CW mm, minimum height=16mm] (r1) at (32.2,-52) {};
\node[card=ORG, minimum width=78mm, minimum height=16mm] (r2) at (127,-52) {};
\node[ttl] at ([yshift=4.3mm]r1.center) {Physiological representation};
\node[sub, align=center] at ([yshift=-1.3mm]r1.center)
      {HRV indices \ \textbullet\ \ EDA phasic and tonic components\\
       time-frequency maps \ \textbullet\ \ learned embeddings};
\node[ttl] at ([yshift=4.3mm]r2.center) {Behavioral representation};
\node[sub, align=center] at ([yshift=-1.3mm]r2.center)
      {action-unit intensities \ \textbullet\ \ blink rate\\
       fixation statistics \ \textbullet\ \ rPPG-derived heart rate};

%% ================= STAGE 4 : FUSION =================
\node[card=TEA, minimum width=179.4mm, minimum height=15mm] (fu) at (76.2,-73) {};
\node[ttl, anchor=west] at ([xshift=4mm,yshift=3.6mm]fu.west) {Fusion stage};
\node[chip=TEA, anchor=west] (f1) at ([xshift=4mm,yshift=-2.6mm]fu.west)
      {feature level (early)};
\node[chip=TEA, right=3mm of f1] (f2) {decision level (late)};
\node[chip=TEA, right=3mm of f2] (f3) {hybrid, multi-stage};
\node[chip=TEA, right=3mm of f3] (f4) {context gated};
\node[sub, anchor=east] at ([xshift=-4mm,yshift=3.6mm]fu.east)
      {median within-study gain \textbf{+4.67 pp}};

%% ================= STAGE 5 : INFERENCE =================
\node[card=BLU, minimum width=179.4mm, minimum height=15mm] (inf) at (76.2,-92) {};
\node[ttl, anchor=west] at ([xshift=4mm,yshift=3.6mm]inf.west) {Inference model};
\node[chip=BLU, anchor=west] (i1) at ([xshift=4mm,yshift=-2.6mm]inf.west)
      {classical ML: RF, XGBoost, SVM};
\node[chip=BLU, right=3mm of i1] (i2) {CNN, LSTM, CNN--LSTM};
\node[chip=BLU, right=3mm of i2] (i3) {transformer, attention};
\node[chip=BLU, right=3mm of i3] (i4) {foundation model};

%% ================= STAGE 6 : EVALUATION (focus) =================
\node[rectangle, rounded corners=1.4mm, draw=RED, fill=RED!7, line width=1.15pt,
      minimum width=179.4mm, minimum height=19mm, inner sep=0pt] (ev) at (76.2,-113) {};
\node[ttl, anchor=west, text=RED!72!black]
      at ([xshift=4mm,yshift=5.2mm]ev.west) {Evaluation protocol};
\node[chip=RED, anchor=west] (e1) at ([xshift=4mm,yshift=-0.6mm]ev.west) {personalized};
\node[chip=RED, right=3mm of e1] (e2) {subject dependent};
\node[chip=RED, right=3mm of e2] (e3) {leave-one-subject-out};
\node[chip=RED, right=3mm of e3] (e4) {cross-dataset};
\node[chip=RED, right=3mm of e4] (e5) {laboratory vs field};
\node[font=\sffamily\itshape\footnotesize, text=RED!72!black, anchor=west]
      at ([xshift=4mm,yshift=-5.9mm]ev.west)
      {this stage, not the fusion stage, sets what a reported accuracy means:
       median within-study swing \textbf{9.14 pp}, up to \textbf{48.66 pp}};

%% ================= STAGE 7 : OUTPUT =================
\node[card=GLD, minimum width=57mm, minimum height=14mm] (o1) at (15,-137) {};
\node[card=GLD, minimum width=57mm, minimum height=14mm] (o2) at (76.2,-137) {};
\node[card=GLD, minimum width=57mm, minimum height=14mm] (o3) at (137.4,-137) {};
\node[ttl] at ([yshift=2.6mm]o1.center) {Stress state and level};
\node[sub] at ([yshift=-1.7mm]o1.center) {binary or graded};
\node[ttl] at ([yshift=2.6mm]o2.center) {Attention and drowsiness};
\node[sub] at ([yshift=-1.7mm]o2.center) {cognitive load, inattention};
\node[ttl] at ([yshift=2.6mm]o3.center) {Closed-loop actuation};
\node[sub] at ([yshift=-1.7mm]o3.center) {feedback, neurostimulation};

%% ================= stage labels =================
\node[stage, minimum height=\SH mm]  at (\LX, 0)    {ACQUIRE};
\node[stage, minimum height=16mm]    at (\LX,-31)   {CONDITION};
\node[stage, minimum height=16mm]    at (\LX,-52)   {REPRESENT};
\node[stage, minimum height=15mm]    at (\LX,-73)   {FUSE};
\node[stage, minimum height=15mm]    at (\LX,-92)   {INFER};
\node[stage, minimum height=19mm, fill=RED!12, text=RED!70!black] at (\LX,-113) {EVALUATE};
\node[stage, minimum height=14mm]    at (\LX,-137)  {DECIDE};

%% ================= flow arrows =================
\draw[flow] (wgrp.south) -- (c1.north);
\draw[flow] (vgrp.south) -- (c2.north);
\draw[flow] (c1) -- (r1);
\draw[flow] (c2) -- (r2);
\draw[flow] (r1.south) -- ++(0,-3) -| ([xshift=-44mm]fu.north);
\draw[flow] (r2.south) -- ++(0,-3) -| ([xshift=44mm]fu.north);
\draw[flow] (fu) -- (inf);
\draw[flow] (inf) -- (ev);
\draw[flow] (ev.south) -- ++(0,-4) -| (o1.north);
\draw[flow] (ev.south) -- ++(0,-4) -| (o2.north);
\draw[flow] (ev.south) -- ++(0,-4) -| (o3.north);
\draw[loop] (o3.east) -- ++(8.5,0) |- ([yshift=-1.5mm]vgrp.east);
\node[font=\sffamily\itshape\footnotesize, text=RED!75, anchor=south, align=center,
      fill=white, inner sep=0.6mm, rotate=90]
      at ([xshift=10mm,yshift=28mm]o3.east) {closed-loop actuation};
\end{tikzpicture}
"""


# =============================================================================
# 12. FIGURE 2  PRISMA flow diagram  (LaTeX / TikZ source)
# =============================================================================
FIG2_TIKZ = r"""\begin{tikzpicture}[node distance=5mm]

\node[pr] (r1) {\textbf{Identification}\\
  Records in the pre-specified source corpus: $n=117$\\
  Duplicate record removed (one study cited twice): $n=1$};

\node[pr,below=6mm of r1] (r2) {\textbf{Screening}\\
  Unique bibliographic records screened: $n=116$\\
  Records with a resolvable DOI and recoverable metadata: $n=116$};

\node[prx,anchor=west] (x1) at ($(r2.east)+(9mm,-6mm)$) {\textbf{Excluded at eligibility appraisal: $n=56$}\\[1pt]
  Outcome outside the stress, attention or cognitive-load scope: $n=41$\\
  No quantitative evaluation of a detection model
  (protocol, review, acceptance or intervention study): $n=10$\\
  Not a peer-reviewed journal article (two preprints, one conference paper): $n=3$\\
  Published outside the 2022--2026 window: $n=2$};

\node[pr,below=6mm of r2] (r3) {\textbf{Eligibility}\\
  Studies meeting all inclusion criteria: $n=60$};

\node[pr,below=6mm of r3] (r4) {\textbf{Verification}\\
  Independent corroboration of the bibliographic record and the
  reported outcome attempted for every included study: $n=60$};

\node[prx,anchor=west] (x2) at ($(r4.east)+(9mm,-6mm)$) {\textbf{Not carried into quantitative synthesis: $n=32$}\\[1pt]
  Headline outcome not recoverable from the openly retrievable
  record (paywalled full text): $n=32$\\
  Bibliographic record corroborated for all 60 included studies; the
  32 are retained in the narrative synthesis only};

\node[pr,below=6mm of r4,fill=acc!10] (r5) {\textbf{Included}\\
  Narrative synthesis: $n=60$ studies\\
  Quantitative synthesis: $n=28$ studies contributing 34 corroborated
  outcome records,\\ 4 within-study fusion contrasts and 10 within-study
  evaluation contrasts};

\draw[ar] (r1) -- (r2);
\draw[ar] (r2) -- (r3);
\draw[ar] (r3) -- (r4);
\draw[ar] (r4) -- (r5);
\draw[ar] ($(r2.south)!0.5!(r3.north)$) -| ($(r2.east)+(4.5mm,0)$) |- (x1.west);
\draw[ar] ($(r4.south)!0.5!(r5.north)$) -| ($(r4.east)+(4.5mm,0)$) |- (x2.west);
\end{tikzpicture}
"""


def figure1(texdir):
    path = os.path.join(texdir, "fig1_block.tex")
    with open(path, "w") as fh:
        fh.write(FIG1_TIKZ)
    print("  wrote", path, "(TikZ; \\input into the manuscript)")


def figure2(texdir):
    path = os.path.join(texdir, "fig2_prisma.tex")
    with open(path, "w") as fh:
        fh.write(FIG2_TIKZ)
    print("  wrote", path, "(TikZ; \\input into the manuscript)")


# =============================================================================
# 13. ENTRY POINT
# =============================================================================
def summary():
    """Print the aggregate statistics quoted in the manuscript text."""
    g = [r["m"] - r["u"] for r in FUSION]
    d = [r["hi"] - r["lo"] for r in PROTOCOL]
    acc = [o["value"] for o in OUTCOMES if o["metric"] == "Accuracy"]
    print("\nAggregate statistics reproduced from the embedded evidence base")
    print("  accuracy records      k = %2d   median %6.2f   IQR %.2f-%.2f"
          % (len(acc), st.median(acc),
             st.quantiles(acc, n=4)[0], st.quantiles(acc, n=4)[2]))
    print("  fusion gain           k = %2d   median %6.2f   range %.2f-%.2f"
          % (len(g), st.median(g), min(g), max(g)))
    print("  evaluation-induced    k = %2d   median %6.2f   range %.2f-%.2f"
          % (len(d), st.median(d), min(d), max(d)))
    for k in ("Personalization", "Deployment setting", "Task granularity",
              "Dataset transfer"):
        v = [r["hi"] - r["lo"] for r in PROTOCOL if r["kind"] == k]
        print("    %-20s k = %2d   median %6.2f" % (k, len(v), st.median(v)))
    print("  corroboration rate    %d/%d = %.1f%%"
          % (len(CORROBORATED), len(ATTEMPTED),
             100 * len(CORROBORATED) / len(ATTEMPTED)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outdir", default="../figures",
                    help="directory for the rendered PNG figures (default ../figures)")
    ap.add_argument("--texdir", default=".",
                    help="directory for the emitted TikZ sources (default .)")
    ap.add_argument("--stats", action="store_true",
                    help="also print the aggregate statistics")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(args.texdir, exist_ok=True)

    print("Figures 1-2 (LaTeX / TikZ):")
    figure1(args.texdir)
    figure2(args.texdir)

    print("Figures 3-10 (matplotlib):")
    for fn in (figure3, figure4, figure5, figure6, figure7, figure8, figure9, figure10):
        fn(args.outdir)

    if args.stats:
        summary()
    print("\nDone: 2 TikZ sources + 8 rendered figures.")


if __name__ == "__main__":
    main()
