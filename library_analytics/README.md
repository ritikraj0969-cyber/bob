# 📚 Library Usage Analytics

A simple Python project that analyzes library book borrowing data using **Pandas** and **Matplotlib**.

---

## Project Structure

```
library_analytics/
├── main.py               ← Entry point — run this
├── analysis.py           ← Data loading & Pandas analytics
├── visualizations.py     ← Matplotlib chart generation
├── data/
│   ├── books.csv         ← 20 books across 8 categories
│   ├── members.csv       ← 20 library members
│   └── borrowings.csv    ← 80 borrow records (Jan–Aug 2024)
└── charts/               ← Generated PNG charts saved here
```

---

## Requirements

```
pandas
matplotlib
```

Install with:

```bash
pip install pandas matplotlib
```

---

## Running

```bash
cd library_analytics
python main.py
```

---

## What It Analyzes

| Analysis | Description |
|---|---|
| **Top Borrowed Books** | Ranks books by number of borrows |
| **Borrows by Category** | Aggregates borrow counts per genre/category |
| **Monthly Trend** | Line chart of borrowing activity per month |
| **Membership Distribution** | Pie chart of Premium / Standard / Student split |
| **Most Active Members** | Members ranked by total borrows |
| **Copies vs Borrows** | Compares available copies to demand per category |
| **Borrow Status** | Donut chart — Active vs Returned borrowings |

---

## Charts Generated

| File | Chart |
|---|---|
| `01_most_borrowed_books.png` | Horizontal bar — top 10 books |
| `02_borrows_by_category.png` | Vertical bar — borrows per category |
| `03_monthly_trend.png` | Line chart — monthly trend |
| `04_membership_distribution.png` | Pie chart — membership types |
| `05_top_active_members.png` | Horizontal bar — active members |
| `06_copies_vs_borrows.png` | Grouped bar — supply vs demand |
| `07_borrow_status.png` | Donut — active vs returned |

---

## Dataset

- **20 books** spanning Fiction, Non-Fiction, Science, Technology, Self-Help, Biography, and History.
- **20 members** with Premium, Standard, and Student memberships.
- **80 borrow records** covering January through August 2024.
