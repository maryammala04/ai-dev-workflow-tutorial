# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo is two things layered together:

1. **A tutorial** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`) that teaches an AI-assisted development workflow: PRD → `TASKS.md` milestones → Superpowers `brainstorming` (design doc) → `writing-plans` (implementation plan) → `executing-plans`/subagent-driven execution (TDD where flagged) → commit → push → deploy.
2. **The actual project being built through that workflow**: a Streamlit e-commerce sales dashboard, specified in `prd/ecommerce-analytics.md`, implemented as `app.py` + `data.py` + `tests/`.

When asked to work on "the dashboard," the relevant files are `app.py`, `data.py`, `tests/test_data.py`, `data/sales-data.csv`, and `requirements.txt` — not the tutorial prose files.

## Commands

```bash
# Activate the virtual environment (created at venv/, already gitignored)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard locally
streamlit run app.py

# Run the full test suite
pytest tests/ -v

# Run a single test
pytest tests/test_data.py::test_compute_total_sales -v

# Re-pin dependencies after adding a new package
pip freeze > requirements.txt
```

## Architecture

**`data.py` / `app.py` split is the core convention.** `data.py` holds only pure functions — DataFrame (or path) in, value or DataFrame out, zero Streamlit calls. `app.py` owns all rendering and Streamlit calls, and consumes `data.py`'s functions. This split exists specifically so the data/aggregation logic is unit-testable without a running Streamlit app; `app.py` itself is verified by running it, not by unit tests. New aggregation logic belongs in `data.py`; new UI/layout belongs in `app.py`.

**Error handling contract:** `load_sales_data` in `data.py` is the single point where file/parse errors are translated into either `FileNotFoundError` (missing file) or `ValueError` (anything else — missing required columns, corrupt content, bad encoding, etc.). `app.py` catches exactly `(FileNotFoundError, ValueError)` around the cached data load and renders a friendly `st.error(...)` + `st.stop()` instead of letting a raw traceback reach the UI. Any new failure mode in `load_sales_data` should be wrapped into one of these two types, not left to propagate.

**Shared chart palette:** `app.py` defines two module-level color constants — `COLOR_ACCENT` (trend line) and `COLOR_NEUTRAL` (both bar charts) — reused across every chart so the dashboard reads as one visual family rather than four independently-colored charts. New charts should reuse these constants rather than introducing new colors ad hoc.

**Data flow is single-pass, not lazy:** `app.py` loads the CSV once (`st.cache_data`-wrapped) and computes every aggregate up front before rendering, rather than each section re-filtering independently. There's no filtering/date-range UI (out of scope per the PRD's Phase 2 list), so this keeps things simple — don't add per-section recomputation without a reason.

## Testing conventions

Every function in `data.py` has a corresponding test in `tests/test_data.py`, built test-first (TDD): write the failing test, confirm it fails for the right reason, implement, confirm it passes. Tests assert on real output values (exact sums, sort order, column names) rather than just type/shape — a test that would pass against a broken implementation is treated as a defect, not coverage. `test_real_dataset_matches_prd_expected_output` is a regression test against the real `data/sales-data.csv`, asserting the exact values from the PRD's "Expected Output" table (482 orders, ~$116,500 total, "Electronics" top category) — if it fails, suspect a bug in a `compute_*` function before changing the assertion.

## Work tracking

`TASKS.md` is the durable, git-committed record of milestone status (To Do / In Progress / Done) — distinct from Claude Code's in-session todo list, which disappears on `/clear`. Every commit that completes milestone work is prefixed with the milestone ID (e.g. `TASK-2: KPI scorecards`), so `git log` traces requirement → code. Design docs live in `docs/superpowers/specs/`, implementation plans in `docs/superpowers/plans/` — both are committed (there's a `.gitignore` carve-out: `docs/*` is ignored except `docs/superpowers/`).

## Deployment

Target is Streamlit Community Cloud, deployed from `main` (`app.py` as the entrypoint). Deployment itself requires the repo owner's own Streamlit/GitHub login and isn't something to script — treat it as a manual handoff step, not an automatable task.
