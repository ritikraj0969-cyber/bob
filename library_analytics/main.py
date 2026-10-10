"""
Library Usage Analytics — Main Entry Point
Run this script to see the console summary and generate all charts.
"""

import sys
from pathlib import Path

# Make sure local modules are importable when run directly
sys.path.insert(0, str(Path(__file__).parent))

from analysis import load_data, print_summary
from visualizations import generate_all_charts


def main():
    print("\nLoading data...")
    books, members, borrowings = load_data()

    # ── Console summary ───────────────────────────────────────────────────────
    print_summary(books, members, borrowings)

    # ── Charts ────────────────────────────────────────────────────────────────
    generate_all_charts(books, members, borrowings)


if __name__ == "__main__":
    main()
