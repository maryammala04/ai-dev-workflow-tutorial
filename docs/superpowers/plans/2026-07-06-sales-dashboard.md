# E-Commerce Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit dashboard (KPI cards, monthly sales trend, category/region breakdowns) from `data/sales-data.csv`, deployable to Streamlit Community Cloud.

**Architecture:** `data.py` holds pure, unit-tested functions (CSV loading/validation, aggregation). `app.py` holds all Streamlit rendering and calls into `data.py`; it is verified by running the app, not by unit tests. `tests/test_data.py` covers everything in `data.py`.

**Tech Stack:** Python 3.11+, Streamlit, Plotly (`plotly.express`), Pandas, pytest.

## Global Constraints

- Python 3.11+ (PRD Technical Approach).
- Only third-party deps: `streamlit`, `pandas`, `plotly`, `pytest` (PRD Technical Approach; pytest is dev-only).
- Currency formatted as `$X,XXX,XXX` (no decimals); large numbers use thousands separators (PRD FR-1).
- Dashboard loads within 5 seconds; charts render within 2 seconds of data load (PRD NFR-1) — use `st.cache_data` on the CSV load so reruns don't re-read the file.
- No filtering/date-range UI, no auth, no export, no drill-down — Phase 2, out of scope for this plan (PRD Phase 2).
- Must be deployable to Streamlit Community Cloud (PRD NFR-5).
- `data.py` contains no Streamlit calls; every function takes a DataFrame in and returns a value out (design doc, Architecture).
- Trend chart aggregates monthly, not daily (design doc, Components & Data Flow).
- Missing or malformed CSV → caught, shown via `st.error(...)`, then `st.stop()` — no raw traceback (design doc, Error Handling).
- TDD (failing test first) applies to every function in `data.py`. Streamlit rendering/layout code in `app.py` is not TDD'd — verified by running the app.
- Work on the current branch `feature/sales-dashboard`; do not create a git worktree.
- Dependencies live in a virtual environment at `venv/` (already gitignored).
- Every commit message is prefixed with the milestone ID it completes (`TASKS.md` Definition of Done), and each milestone's `TASKS.md` entry moves from To Do to Done in the same commit.

---

### Task 1: Environment Setup and Data Loading

**Files:**
- Create: `requirements.txt`
- Create: `data.py`
- Create: `tests/test_data.py`
- Create: `app.py`
- Modify: `TASKS.md` (move TASK-1 to Done)

**Interfaces:**
- Produces: `load_sales_data(path: str) -> pd.DataFrame`, raising `FileNotFoundError` (missing file) or `ValueError` (missing required columns). Required columns: `date, order_id, product, category, region, quantity, unit_price, total_amount`.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`
Expected: a `venv/` directory is created (already covered by `.gitignore`).

- [ ] **Step 2: Activate it and create `requirements.txt`**

Run: `source venv/bin/activate` (macOS/Linux)

Create `requirements.txt`:

```
streamlit
pandas
plotly
pytest
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: install completes with no errors.

- [ ] **Step 4: Write the failing test for a missing file**

Create `tests/test_data.py`:

```python
import pandas as pd
import pytest

from data import load_sales_data

VALID_CSV = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-03,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98
2024-01-04,ORD-002,Phone Case,Accessories,South,3,24.99,74.97
"""


def test_load_sales_data_missing_file(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_sales_data(str(missing_path))
```

- [ ] **Step 5: Run it to verify it fails**

Run: `pytest tests/test_data.py::test_load_sales_data_missing_file -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'data'` (file doesn't exist yet).

- [ ] **Step 6: Create `data.py` with just enough to pass**

```python
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(path):
    try:
        df = pd.read_csv(path, parse_dates=["date"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at {path}")

    return df
```

- [ ] **Step 7: Run it to verify it passes**

Run: `pytest tests/test_data.py::test_load_sales_data_missing_file -v`
Expected: PASS

- [ ] **Step 8: Write the failing test for missing columns**

Add to `tests/test_data.py`:

```python
def test_load_sales_data_missing_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text(
        "date,order_id,product,category,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Wireless Earbuds,Audio,2,79.99,159.98\n"
    )  # missing "region"

    with pytest.raises(ValueError, match="region"):
        load_sales_data(str(csv_path))
```

- [ ] **Step 9: Run it to verify it fails**

Run: `pytest tests/test_data.py::test_load_sales_data_missing_columns -v`
Expected: FAIL (no `ValueError` is raised — column validation doesn't exist yet)

- [ ] **Step 10: Implement column validation**

Modify `data.py`, replacing the `load_sales_data` function:

```python
def load_sales_data(path):
    try:
        df = pd.read_csv(path, parse_dates=["date"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at {path}")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    return df
```

- [ ] **Step 11: Run both tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: 2 passed

- [ ] **Step 12: Write and run the success-path test**

Add to `tests/test_data.py`:

```python
def test_load_sales_data_success(tmp_path):
    csv_path = tmp_path / "good.csv"
    csv_path.write_text(VALID_CSV)

    df = load_sales_data(str(csv_path))

    assert len(df) == 2
    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
```

Run: `pytest tests/test_data.py -v`
Expected: 3 passed

- [ ] **Step 13: Create the minimal `app.py`**

```python
import streamlit as st

from data import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def get_data():
    return load_sales_data(DATA_PATH)


try:
    df = get_data()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

st.write(f"Loaded {len(df):,} transactions.")
```

- [ ] **Step 14: Run the app and verify it works**

Run: `streamlit run app.py`
Expected: browser opens `http://localhost:8501`, shows the title "ShopSmart Sales Dashboard" and "Loaded 482 transactions." with no errors. Stop it with Ctrl+C when done.

- [ ] **Step 15: Update `TASKS.md` and commit**

In `TASKS.md`, move the `TASK-1` entry (with its acceptance-criteria checkboxes checked) from `## To Do` to `## Done`.

Run:
```bash
git add requirements.txt data.py app.py tests/test_data.py TASKS.md
git commit -m "TASK-1: project setup and data loading"
```

---

### Task 2: KPI Scorecards

**Files:**
- Modify: `data.py` (add `compute_total_sales`, `compute_total_orders`)
- Modify: `tests/test_data.py`
- Modify: `app.py` (render the two metric cards)
- Modify: `TASKS.md` (move TASK-2 to Done)

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 1)
- Produces: `compute_total_sales(df: pd.DataFrame) -> float`, `compute_total_orders(df: pd.DataFrame) -> int`

- [ ] **Step 1: Write failing tests for the KPI functions**

Add to `tests/test_data.py`:

```python
import pandas as pd


def _kpi_fixture():
    return pd.DataFrame({
        "total_amount": [100.0, 250.5, 49.5],
    })


def test_compute_total_sales():
    from data import compute_total_sales
    assert compute_total_sales(_kpi_fixture()) == 400.0


def test_compute_total_orders():
    from data import compute_total_orders
    assert compute_total_orders(_kpi_fixture()) == 3
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_data.py -k "kpi or total_sales or total_orders" -v`
Expected: FAIL with `ImportError: cannot import name 'compute_total_sales'`

- [ ] **Step 3: Implement both functions**

Add to `data.py`:

```python
def compute_total_sales(df):
    return df["total_amount"].sum()


def compute_total_orders(df):
    return len(df)
```

- [ ] **Step 4: Run to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: 5 passed

- [ ] **Step 5: Render the KPI cards in `app.py`**

Modify `app.py`, replacing the `st.write(f"Loaded {len(df):,} transactions.")` line with:

```python
from data import (
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)

# ...(after the try/except block that defines df)...

total_sales = compute_total_sales(df)
total_orders = compute_total_orders(df)

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
```

Update the `from data import ...` line at the top of `app.py` to include the new names:

```python
from data import compute_total_orders, compute_total_sales, load_sales_data
```

- [ ] **Step 6: Run the app and verify it works**

Run: `streamlit run app.py`
Expected: two metric cards show "Total Sales" ≈ `$116,500` and "Total Orders" `482`, matching the PRD's Expected Output table. Stop with Ctrl+C.

- [ ] **Step 7: Update `TASKS.md` and commit**

Move `TASK-2` to `## Done` in `TASKS.md`.

```bash
git add data.py app.py tests/test_data.py TASKS.md
git commit -m "TASK-2: KPI scorecards"
```

---

### Task 3: Sales Trend Chart

**Files:**
- Modify: `data.py` (add `compute_monthly_trend`)
- Modify: `tests/test_data.py`
- Modify: `app.py` (render the line chart)
- Modify: `TASKS.md` (move TASK-3 to Done)

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 1)
- Produces: `compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame` with columns `month` (datetime, month start) and `total_sales` (float), sorted chronologically.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_data.py`:

```python
def test_compute_monthly_trend():
    from data import compute_monthly_trend

    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10"]),
        "total_amount": [100.0, 50.0, 75.0],
    })

    result = compute_monthly_trend(df)

    assert list(result["total_sales"]) == [150.0, 75.0]
    assert result["month"].is_monotonic_increasing
```

- [ ] **Step 2: Run to verify it fails**

Run: `pytest tests/test_data.py::test_compute_monthly_trend -v`
Expected: FAIL with `ImportError: cannot import name 'compute_monthly_trend'`

- [ ] **Step 3: Implement the function**

Add to `data.py`:

```python
def compute_monthly_trend(df):
    return (
        df.set_index("date")
        .resample("MS")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "month", "total_amount": "total_sales"})
    )
```

- [ ] **Step 4: Run to verify it passes**

Run: `pytest tests/test_data.py -v`
Expected: 6 passed

- [ ] **Step 5: Render the trend chart in `app.py`**

Add near the top of `app.py`:

```python
import plotly.express as px
```

Add to the `from data import ...` line:

```python
from data import (
    compute_category_breakdown,
    compute_monthly_trend,
    compute_region_breakdown,
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)
```

Add a shared color constant near the top of `app.py` (below `DATA_PATH`):

```python
COLOR_ACCENT = "#2C5F8A"    # trend line - the headline metric
COLOR_NEUTRAL = "#7C93A8"   # category + region bars - shared so both breakdowns read as one family
```

Add after the KPI columns block:

```python
monthly_trend = compute_monthly_trend(df)

st.subheader("Sales Trend Over Time")
trend_fig = px.line(
    monthly_trend, x="month", y="total_sales", markers=True,
    color_discrete_sequence=[COLOR_ACCENT],
)
trend_fig.update_layout(
    xaxis_title="Month", yaxis_title="Sales ($)",
    hovermode="x unified",
)
st.plotly_chart(trend_fig, use_container_width=True)
```

- [ ] **Step 6: Run the app and verify it works**

Run: `streamlit run app.py`
Expected: a line chart appears below the KPI cards showing ~12 monthly points, hovering shows exact values. Stop with Ctrl+C.

- [ ] **Step 7: Update `TASKS.md` and commit**

Move `TASK-3` to `## Done` in `TASKS.md`.

```bash
git add data.py app.py tests/test_data.py TASKS.md
git commit -m "TASK-3: sales trend chart"
```

---

### Task 4: Category and Region Breakdowns

**Files:**
- Modify: `data.py` (add `compute_category_breakdown`, `compute_region_breakdown`)
- Modify: `tests/test_data.py`
- Modify: `app.py` (render the two bar charts)
- Modify: `TASKS.md` (move TASK-4 to Done)

**Interfaces:**
- Consumes: `load_sales_data(path) -> pd.DataFrame` (Task 1)
- Produces: `compute_category_breakdown(df) -> pd.DataFrame` and `compute_region_breakdown(df) -> pd.DataFrame`, each with columns `category`/`region` and `total_sales`, sorted descending by `total_sales`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_data.py`:

```python
def test_compute_category_breakdown():
    from data import compute_category_breakdown

    df = pd.DataFrame({
        "category": ["Electronics", "Electronics", "Accessories", "Audio"],
        "total_amount": [100.0, 50.0, 200.0, 30.0],
    })

    result = compute_category_breakdown(df)

    assert list(result["category"]) == ["Accessories", "Electronics", "Audio"]
    assert list(result["total_sales"]) == [200.0, 150.0, 30.0]


def test_compute_region_breakdown():
    from data import compute_region_breakdown

    df = pd.DataFrame({
        "region": ["North", "South", "East"],
        "total_amount": [120.0, 300.0, 60.0],
    })

    result = compute_region_breakdown(df)

    assert list(result["region"]) == ["South", "North", "East"]
    assert list(result["total_sales"]) == [300.0, 120.0, 60.0]
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_data.py -k breakdown -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement both functions**

Add to `data.py`:

```python
def compute_category_breakdown(df):
    return (
        df.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )


def compute_region_breakdown(df):
    return (
        df.groupby("region")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: 8 passed

- [ ] **Step 5: Render the bar charts in `app.py`**

Add after the trend chart block:

```python
category_breakdown = compute_category_breakdown(df)
region_breakdown = compute_region_breakdown(df)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    category_fig = px.bar(
        category_breakdown, x="category", y="total_sales",
        color_discrete_sequence=[COLOR_NEUTRAL],
    )
    category_fig.update_layout(xaxis_title="", yaxis_title="Sales ($)")
    st.plotly_chart(category_fig, use_container_width=True)

with col4:
    st.subheader("Sales by Region")
    region_fig = px.bar(
        region_breakdown, x="region", y="total_sales",
        color_discrete_sequence=[COLOR_NEUTRAL],
    )
    region_fig.update_layout(xaxis_title="", yaxis_title="Sales ($)")
    st.plotly_chart(region_fig, use_container_width=True)
```

- [ ] **Step 6: Run the app and verify it works**

Run: `streamlit run app.py`
Expected: two bar charts side by side, categories/regions sorted highest-to-lowest, hover shows exact values, "Electronics" is the tallest category bar per the PRD's Expected Output. Stop with Ctrl+C.

- [ ] **Step 7: Update `TASKS.md` and commit**

Move `TASK-4` to `## Done` in `TASKS.md`.

```bash
git add data.py app.py tests/test_data.py TASKS.md
git commit -m "TASK-4: category and region breakdowns"
```

---

### Task 5: Test and Refine

**This is the last task an agent/implementer executes.** It ends with the branch pushed and ready for review. Everything after this task — merging to `main` and deploying — is a separate, human-executed handoff (see "Deployment" below), not part of this task.

**Files:**
- Modify: `tests/test_data.py` (add an end-to-end sanity check against the real CSV)
- Modify: `TASKS.md` (move TASK-5's testing/refinement checkbox items; leave the milestone in progress if deployment is still pending)

**Interfaces:**
- Consumes: every function in `data.py` (Tasks 1-4), the real file at `data/sales-data.csv`.

- [ ] **Step 1: Add an end-to-end regression test against the real data**

Add to `tests/test_data.py`:

```python
def test_real_dataset_matches_prd_expected_output():
    df = load_sales_data("data/sales-data.csv")

    assert compute_total_orders(df) == 482
    assert round(compute_total_sales(df), -2) == 116500  # PRD: ~$116,500

    top_category = compute_category_breakdown(df).iloc[0]["category"]
    assert top_category == "Electronics"
```

Add the missing imports at the top of `tests/test_data.py` if not already present:

```python
from data import (
    compute_category_breakdown,
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)
```

- [ ] **Step 2: Run the full test suite**

Run: `pytest tests/ -v`
Expected: 9 passed. If `test_real_dataset_matches_prd_expected_output` fails, check the actual computed values and compare against `prd/ecommerce-analytics.md`'s "Expected Output" table before changing the assertion — a mismatch likely means a bug in one of the `compute_*` functions, not a wrong expectation.

- [ ] **Step 3: Manually verify against the PRD's Acceptance Criteria**

Run: `streamlit run app.py` and check off each item from `prd/ecommerce-analytics.md`'s Acceptance Criteria section:
- KPIs visible (Total Sales, Total Orders)
- Trend chart shows correct data
- Category chart sorted descending
- Region chart sorted descending
- No errors or warnings in the terminal or browser console
- Dashboard looks presentable at a normal browser window width

Stop the app with Ctrl+C when done.

- [ ] **Step 4: Test the missing-file error path manually**

Temporarily rename the data file, confirm the friendly error appears, then restore it:

```bash
mv data/sales-data.csv data/sales-data.csv.bak
streamlit run app.py   # confirm st.error message appears, no traceback; Ctrl+C to stop
mv data/sales-data.csv.bak data/sales-data.csv
```

- [ ] **Step 5: Freeze dependency versions**

Run: `pip freeze > requirements.txt`
Expected: `requirements.txt` now has exact pinned versions (e.g. `streamlit==1.x.x`) instead of bare package names — this makes the Streamlit Cloud deployment reproducible.

- [ ] **Step 6: Update `TASKS.md`, commit, and push**

Since deployment (below) hasn't happened yet, `TASK-5`'s milestone stays out of `## Done` for now — check off what's actually true (testing/refinement complete) without checking off deployment.

```bash
git add tests/test_data.py requirements.txt TASKS.md
git commit -m "TASK-5: testing and refinement"
git push -u origin feature/sales-dashboard
```

**This is the end of the implementation plan.** Everything below is out of scope for an agent to execute.

---

## Deployment (Human — Execute After Merge)

This section is not part of any implementation task. It requires signing in with your own accounts (GitHub, Streamlit Community Cloud) and is yours to run after the branch above is merged. The plan stops here and hands off to you.

1. **Merge `feature/sales-dashboard` to `main`** — review the diff, then either open a PR or merge locally per your usual workflow (the `finishing-a-development-branch` skill can guide this).
2. **Push `main`** (with the merged dashboard code) to your GitHub fork, if not already up to date.
3. Go to `share.streamlit.io`, sign in with GitHub, click "New app".
4. Select your repo, branch `main`, main file path `app.py`.
5. Click "Deploy" and wait for the build to finish.
6. Confirm the public URL loads the dashboard with no errors.
7. Add the deployed URL to `TASKS.md`'s `TASK-5` entry (move it to `## Done`) and to `README.md`, then commit and push that final update yourself:
   ```bash
   git add TASKS.md README.md
   git commit -m "TASK-5: add deployed dashboard URL"
   git push
   ```

---

## Self-Review Notes

- **Spec coverage:** FR-1 (KPIs) → Task 2. FR-2 (trend) → Task 3. FR-3/FR-4 (category/region) → Task 4. FR-5 (CSV load) → Task 1. NFR-1 (load/render speed) → `st.cache_data` in Task 1. NFR-2 (professional appearance, no training) → shared palette (Task 3/4), clean KPI formatting (Task 2). NFR-3 (modular, maintainable) → `data.py`/`app.py` split, established in Task 1. NFR-5 (deployable) → Deployment section (human-executed, final step of the plan). Acceptance Criteria → Task 5, Step 3. Expected Output values → Task 5, Step 1 regression test.
- **Placeholder scan:** no TBD/TODO; every step has runnable code or an explicit manual instruction (deployment steps are inherently manual — flagged as such rather than left vague).
- **Type consistency:** `compute_*` function names and return shapes (DataFrame with `month`/`category`/`region` + `total_sales`, or scalar) are consistent between where they're defined (Tasks 2-4) and where `app.py` consumes them (same tasks' rendering steps).
