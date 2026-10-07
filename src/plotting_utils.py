"""Shared chart style for the Kathmandu lockdown air-quality project.

Usage (from a notebook in notebooks/):
    import sys; sys.path.append("../src")
    from plotting_utils import set_style, save, COLORS
    set_style()
    fig, ax = plt.subplots(layout="constrained")
    ...
    save(fig, "01_main_finding")      # -> figures/01_main_finding.png at 300 dpi

Colours: one accent (2020, the year being tested) against grey context, plus one
second colour for a second category (e.g. the other station). The accent/second
pair was checked for colour-vision deficiency (CVD) separation, normal-vision
separation and contrast against a white background.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# Folder the figures are written to: <project root>/figures (works from any working directory)
FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"

COLORS = {
    "accent": "#D55E00",      # 2020 / the finding (Okabe-Ito vermillion)
    "second": "#0072B2",      # a second category, e.g. Embassy station (Okabe-Ito blue)
    "context": "#9A9A9A",     # baseline / background data
    "context_dark": "#5E5E5E",
    "context_light": "#C8C8C8",
    "ink": "#222222",         # text
    "muted": "#666666",       # secondary text, annotations
    "grid": "#E6E6E6",
}

# One grey per baseline year (context, not categories: each line is also labelled directly)
YEAR_COLORS = {2017: "#C8C8C8", 2018: "#9A9A9A", 2019: "#5E5E5E", 2020: COLORS["accent"]}


def set_style() -> None:
    """Apply the project's chart style to every figure made afterwards."""
    mpl.rcParams.update({
        "figure.figsize": (8, 4.5),
        "figure.dpi": 110,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 10,
        "axes.labelcolor": COLORS["ink"],
        "axes.edgecolor": "#BBBBBB",
        "axes.spines.top": False,          # no box: only the axes that carry information
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": COLORS["grid"],
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,            # grid behind the data
        "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"],
        "text.color": COLORS["ink"],
        "legend.frameon": False,
        "lines.linewidth": 2,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    })


def save(fig, name: str, folder: Path = FIGURES_DIR) -> Path:
    """Save a figure as <folder>/<name>.png at 300 dpi and return the path."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    print(f"saved {path.relative_to(folder.parent)}")
    return path


def titles(ax, title: str, sub: str = "") -> None:
    """Title that states the finding, plus an optional smaller grey subtitle
    (units, data source, what the marks mean) underneath it."""
    ax.set_title(title, pad=24 if sub else 8)
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=9,
                color=COLORS["muted"], va="bottom", ha="left")
