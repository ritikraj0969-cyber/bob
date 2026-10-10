"""
Library Usage Analytics — Data Analysis Module
Loads and analyzes book borrowing, members, and trends using Pandas.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all three CSV datasets and parse dates."""
    books = pd.read_csv(DATA_DIR / "books.csv")
    members = pd.read_csv(DATA_DIR / "members.csv", parse_dates=["join_date"])
    borrowings = pd.read_csv(
        DATA_DIR / "borrowings.csv",
        parse_dates=["borrow_date", "return_date"],
    )
    return books, members, borrowings


def most_borrowed_books(borrowings: pd.DataFrame, books: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return the top N most borrowed books."""
    counts = borrowings["book_id"].value_counts().reset_index()
    counts.columns = ["book_id", "borrow_count"]
    result = counts.merge(books[["book_id", "title", "category"]], on="book_id")
    return result.head(top_n)


def borrowings_by_category(borrowings: pd.DataFrame, books: pd.DataFrame) -> pd.DataFrame:
    """Return total borrows per book category."""
    merged = borrowings.merge(books[["book_id", "category"]], on="book_id")
    return (
        merged.groupby("category")
        .size()
        .reset_index(name="borrow_count")
        .sort_values("borrow_count", ascending=False)
    )


def monthly_borrowing_trend(borrowings: pd.DataFrame) -> pd.DataFrame:
    """Return borrow counts grouped by month."""
    df = borrowings.copy()
    df["month"] = df["borrow_date"].dt.to_period("M")
    trend = df.groupby("month").size().reset_index(name="borrow_count")
    trend["month"] = trend["month"].astype(str)
    return trend


def membership_distribution(members: pd.DataFrame) -> pd.DataFrame:
    """Return member counts per membership type."""
    df = (
        members["membership_type"]
        .value_counts()
        .reset_index()
    )
    # pandas 3.x: columns are ["membership_type", "count"]
    df.columns = ["membership_type", "member_count"]
    return df


def top_active_members(borrowings: pd.DataFrame, members: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return top N members by number of borrows."""
    counts = borrowings["member_id"].value_counts().reset_index()
    counts.columns = ["member_id", "borrow_count"]
    result = counts.merge(members[["member_id", "name", "membership_type"]], on="member_id")
    return result.head(top_n)


def average_loan_duration(borrowings: pd.DataFrame) -> float:
    """Return average loan duration in days for returned books."""
    returned = borrowings.dropna(subset=["return_date"]).copy()
    returned["loan_days"] = (returned["return_date"] - returned["borrow_date"]).dt.days
    return round(returned["loan_days"].mean(), 1)


def active_vs_returned(borrowings: pd.DataFrame) -> pd.Series:
    """Return count of Active vs Returned borrowings."""
    return borrowings["status"].value_counts()


def category_copies_vs_borrows(borrowings: pd.DataFrame, books: pd.DataFrame) -> pd.DataFrame:
    """Compare total copies available vs total borrows per category."""
    copies = books.groupby("category")["total_copies"].sum().reset_index()
    borrows = borrowings.merge(books[["book_id", "category"]], on="book_id")
    borrow_counts = borrows.groupby("category").size().reset_index(name="borrow_count")
    return copies.merge(borrow_counts, on="category").sort_values("borrow_count", ascending=False)


def print_summary(books, members, borrowings):
    """Print a readable analytics summary to the console."""
    print("=" * 60)
    print("       LIBRARY USAGE ANALYTICS -- SUMMARY REPORT")
    print("=" * 60)

    print(f"\n  Total Books         : {len(books)}")
    print(f"  Total Members       : {len(members)}")
    print(f"  Total Borrowings    : {len(borrowings)}")
    print(f"  Avg Loan Duration   : {average_loan_duration(borrowings)} days")

    status = active_vs_returned(borrowings)
    print(f"  Returned            : {status.get('Returned', 0)}")
    print(f"  Currently Active    : {status.get('Active', 0)}")

    print("\n-- Top 5 Most Borrowed Books --")
    top_books = most_borrowed_books(borrowings, books, top_n=5)
    for _, row in top_books.iterrows():
        print(f"  {row['title'][:40]:<40}  {row['borrow_count']} borrows  [{row['category']}]")

    print("\n-- Borrows by Category --")
    by_cat = borrowings_by_category(borrowings, books)
    for _, row in by_cat.iterrows():
        bar = "#" * row["borrow_count"]
        print(f"  {row['category']:<15}  {row['borrow_count']:>3}  {bar}")

    print("\n-- Membership Distribution --")
    membership = membership_distribution(members)
    for _, row in membership.iterrows():
        print(f"  {row['membership_type']:<12}  {row['member_count']} members")

    print("\n-- Top 5 Most Active Members --")
    top_members = top_active_members(borrowings, members, top_n=5)
    for _, row in top_members.iterrows():
        print(f"  {row['name']:<20}  {row['borrow_count']} borrows  [{row['membership_type']}]")

    print("\n" + "=" * 60)
