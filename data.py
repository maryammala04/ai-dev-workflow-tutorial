import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(path):
    try:
        df = pd.read_csv(path, parse_dates=["date"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at {path}") from None
    except Exception as e:
        # Any other read/parse failure (corrupt file, bad encoding, a CSV
        # missing the "date" column itself) should surface as the same
        # friendly error app.py already catches, not a raw traceback.
        raise ValueError(f"Could not parse CSV at {path}: {e}") from e

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    return df


def compute_total_sales(df):
    return df["total_amount"].sum()


def compute_total_orders(df):
    return len(df)


def compute_monthly_trend(df):
    return (
        df.set_index("date")
        .resample("MS")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "month", "total_amount": "total_sales"})
    )


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
