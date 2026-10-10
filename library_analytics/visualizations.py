"""
Library Usage Analytics — Visualization Module
Generates and saves charts using Matplotlib.
"""

import matplotlib
matplotlib.use("Agg")          # headless backend — safe for all environments
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from pathlib import Path

CHARTS_DIR = Path(__file__).parent / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

# ── Shared style ─────────────────────────────────────────────────────────────
PALETTE = ["#3b82d4", "#7c5cd8", "#22c55e", "#f59e0b", "#ef4444",
           "#06b6d4", "#ec4899", "#84cc16"]
TITLE_FONT  = {"fontsize": 13, "fontweight": "bold", "color": "#1f2328"}
LABEL_FONT  = {"fontsize": 10, "color": "#57606a"}
TICK_COLOR  = "#57606a"
GRID_COLOR  = "#e5e7eb"
BG_COLOR    = "#f7f8fa"


def _apply_base_style(ax, title: str, xlabel: str = "", ylabel: str = ""):
    ax.set_facecolor(BG_COLOR)
    ax.figure.patch.set_facecolor("#ffffff")
    ax.set_title(title, **TITLE_FONT, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, **LABEL_FONT)
    if ylabel:
        ax.set_ylabel(ylabel, **LABEL_FONT)
    ax.tick_params(colors=TICK_COLOR, labelsize=9)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)


def chart_most_borrowed_books(top_books: pd.DataFrame):
    """Horizontal bar chart — top 10 most borrowed books."""
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(top_books))]
    bars = ax.barh(
        top_books["title"].str[:35],
        top_books["borrow_count"],
        color=colors, edgecolor="white", linewidth=0.5
    )
    ax.invert_yaxis()
    _apply_base_style(ax, "Top 10 Most Borrowed Books", xlabel="Number of Borrows")
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.yaxis.grid(False)
    for bar, val in zip(bars, top_books["borrow_count"]):
        ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9, color="#1f2328")
    plt.tight_layout()
    path = CHARTS_DIR / "01_most_borrowed_books.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_borrows_by_category(by_cat: pd.DataFrame):
    """Vertical bar chart — borrows per category."""
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = PALETTE[: len(by_cat)]
    bars = ax.bar(
        by_cat["category"],
        by_cat["borrow_count"],
        color=colors, edgecolor="white", linewidth=0.5, zorder=3
    )
    _apply_base_style(ax, "Borrowings by Book Category",
                      xlabel="Category", ylabel="Number of Borrows")
    ax.tick_params(axis="x", rotation=20)
    for bar, val in zip(bars, by_cat["borrow_count"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                str(val), ha="center", fontsize=9, color="#1f2328")
    plt.tight_layout()
    path = CHARTS_DIR / "02_borrows_by_category.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_monthly_trend(trend: pd.DataFrame):
    """Line chart — monthly borrowing trend."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        trend["month"], trend["borrow_count"],
        marker="o", linewidth=2.2, color=PALETTE[0],
        markersize=7, markerfacecolor="white", markeredgewidth=2
    )
    ax.fill_between(trend["month"], trend["borrow_count"],
                    alpha=0.12, color=PALETTE[0])
    _apply_base_style(ax, "Monthly Borrowing Trend (2024)",
                      xlabel="Month", ylabel="Number of Borrows")
    ax.tick_params(axis="x", rotation=30)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    for x, y in zip(trend["month"], trend["borrow_count"]):
        ax.annotate(str(y), (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8, color="#1f2328")
    plt.tight_layout()
    path = CHARTS_DIR / "03_monthly_trend.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_membership_pie(membership: pd.DataFrame):
    """Pie chart — membership type distribution."""
    fig, ax = plt.subplots(figsize=(7, 6))
    wedge_props = {"edgecolor": "white", "linewidth": 2}
    wedges, texts, autotexts = ax.pie(
        membership["member_count"],
        labels=membership["membership_type"],
        colors=PALETTE[: len(membership)],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=wedge_props,
        pctdistance=0.75,
    )
    for text in texts:
        text.set_fontsize(11)
        text.set_color("#1f2328")
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title("Membership Type Distribution", **TITLE_FONT, pad=14)
    fig.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    path = CHARTS_DIR / "04_membership_distribution.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_top_members(top_members: pd.DataFrame):
    """Horizontal bar chart — top active members."""
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(top_members))]
    bars = ax.barh(
        top_members["name"],
        top_members["borrow_count"],
        color=colors, edgecolor="white", linewidth=0.5
    )
    ax.invert_yaxis()
    _apply_base_style(ax, "Top 10 Most Active Members", xlabel="Number of Borrows")
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.yaxis.grid(False)
    for bar, val in zip(bars, top_members["borrow_count"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9, color="#1f2328")
    plt.tight_layout()
    path = CHARTS_DIR / "05_top_active_members.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_copies_vs_borrows(cmp: pd.DataFrame):
    """Grouped bar chart — available copies vs total borrows per category."""
    x = range(len(cmp))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar([i - width / 2 for i in x], cmp["total_copies"],
                width, label="Total Copies", color=PALETTE[0],
                edgecolor="white", zorder=3)
    b2 = ax.bar([i + width / 2 for i in x], cmp["borrow_count"],
                width, label="Total Borrows", color=PALETTE[1],
                edgecolor="white", zorder=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(cmp["category"], rotation=20, ha="right")
    _apply_base_style(ax, "Copies Available vs Total Borrows by Category",
                      xlabel="Category", ylabel="Count")
    ax.legend(fontsize=9, framealpha=0.7)
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                str(int(bar.get_height())), ha="center", fontsize=8, color="#1f2328")
    plt.tight_layout()
    path = CHARTS_DIR / "06_copies_vs_borrows.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def chart_borrow_status(status: pd.Series):
    """Donut chart — active vs returned borrowings."""
    fig, ax = plt.subplots(figsize=(6, 6))
    wedge_props = {"edgecolor": "white", "linewidth": 3, "width": 0.5}
    colors = [PALETTE[2], PALETTE[3]]
    wedges, texts, autotexts = ax.pie(
        status.values,
        labels=status.index,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=wedge_props,
        pctdistance=0.75,
    )
    for text in texts:
        text.set_fontsize(11)
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.text(0, 0, f"{sum(status.values)}\nTotal", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#1f2328")
    ax.set_title("Borrow Status: Active vs Returned", **TITLE_FONT, pad=14)
    fig.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    path = CHARTS_DIR / "07_borrow_status.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔  Saved: {path.name}")


def generate_all_charts(books, members, borrowings):
    """Run all chart generators and save to charts/."""
    from analysis import (
        most_borrowed_books, borrowings_by_category, monthly_borrowing_trend,
        membership_distribution, top_active_members,
        category_copies_vs_borrows, active_vs_returned,
    )
    print("\nGenerating charts...")
    chart_most_borrowed_books(most_borrowed_books(borrowings, books))
    chart_borrows_by_category(borrowings_by_category(borrowings, books))
    chart_monthly_trend(monthly_borrowing_trend(borrowings))
    chart_membership_pie(membership_distribution(members))
    chart_top_members(top_active_members(borrowings, members))
    chart_copies_vs_borrows(category_copies_vs_borrows(borrowings, books))
    chart_borrow_status(active_vs_returned(borrowings))
    print(f"\n✅  All 7 charts saved to  →  {CHARTS_DIR}\n")
