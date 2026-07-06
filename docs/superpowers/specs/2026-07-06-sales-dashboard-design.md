# Design: E-Commerce Sales Dashboard

Source: `prd/ecommerce-analytics.md` (Phase 1 scope only). Tracked in `TASKS.md` as TASK-1 through TASK-5.

## Architecture & File Layout

```
app.py              # Streamlit UI: layout, rendering, error display
data.py             # Pure functions: load + validate CSV, compute aggregates
tests/test_data.py  # pytest unit tests for data.py functions
requirements.txt    # streamlit, pandas, plotly, pytest
venv/               # virtual environment (gitignored)
```

`data.py` contains no Streamlit calls. Every function takes a DataFrame in and returns a value out, so it can be unit-tested without a running app. `app.py` owns all rendering and is not unit-tested directly; it's verified by running the app.

## Components & Data Flow

**`data.py`:**
- `load_sales_data(path)` — reads `data/sales-data.csv`, parses `date` as datetime, validates required columns are present. Raises `FileNotFoundError` if the file is missing, `ValueError` (naming the missing columns) if the schema doesn't match.
- `compute_total_sales(df)` — sum of `total_amount`.
- `compute_total_orders(df)` — count of transactions.
- `compute_monthly_trend(df)` — sales aggregated by calendar month, chronologically ordered.
- `compute_category_breakdown(df)` — sales by category, sorted descending.
- `compute_region_breakdown(df)` — sales by region, sorted descending.

**`app.py`:**
- Loads data once via `st.cache_data(load_sales_data)`.
- Calls each `compute_*` function once, up front (single-pass compute — no per-section re-filtering, since Phase 1 has no filter UI).
- Renders, top to bottom:
  1. Title
  2. Two `st.metric` cards side by side (`st.columns(2)`): Total Sales (formatted `$X,XXX,XXX`), Total Orders (formatted with thousands separator)
  3. Plotly line chart: monthly sales trend, with hover tooltips showing exact values
  4. Two Plotly bar charts side by side (`st.columns(2)`): category breakdown and region breakdown, both sorted descending, both with hover tooltips

**Trend chart granularity:** monthly (not daily). With 482 transactions over 12 months, monthly aggregation (~12 points) reads as a clean trend line; daily (365 points) would be noisy and harder to read in an executive-facing view.

## Error Handling

- **Missing file:** `load_sales_data` raises `FileNotFoundError` with a clear message. `app.py` catches it, shows `st.error("Data file not found at data/sales-data.csv")`, and calls `st.stop()` — no traceback, no partial dashboard render.
- **Malformed/incomplete CSV:** `load_sales_data` validates that all required columns (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`) are present after reading. Raises `ValueError` naming the missing columns; caught and displayed the same way as a missing file.
- No other error handling is needed. Phase 1 has no user input (no filters, no forms, no auth — all out of scope per the PRD), so the CSV load is the only failure surface.

## Testing

- `tests/test_data.py` (pytest) exercises the `compute_*` and `load_sales_data` functions against a small fixture DataFrame:
  - `compute_total_sales` / `compute_total_orders` return correct values for known input
  - `compute_monthly_trend` aggregates correctly and returns months in chronological order
  - `compute_category_breakdown` / `compute_region_breakdown` are sorted descending by sales value
  - `load_sales_data` raises `FileNotFoundError` on a missing path and `ValueError` on missing columns
- Chart rendering (Plotly figure construction, `st.metric`/`st.plotly_chart` calls) is not unit-tested — Streamlit components have no meaningful return value to assert against. Verified manually via `streamlit run app.py`, per the Definition of Done in `TASKS.md`.

## Styling

One shared categorical color palette (muted blue/gray tones plus a single accent color) is defined once and reused across the trend line and both bar charts, so all four visuals read as one cohesive dashboard rather than four independently-styled charts. This directly serves NFR-2's "professional appearance suitable for executive presentations."

## Out of Scope (Phase 2, per PRD)

Filtering/date range selection, drill-down, auth, real-time DB integration, export, email alerts, mobile-responsive design.
