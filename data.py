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

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    return df
