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


def test_load_sales_data_missing_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text(
        "date,order_id,product,category,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Wireless Earbuds,Audio,2,79.99,159.98\n"
    )  # missing "region"

    with pytest.raises(ValueError, match="region"):
        load_sales_data(str(csv_path))


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


def test_load_sales_data_corrupt_content(tmp_path):
    csv_path = tmp_path / "corrupt.csv"
    csv_path.write_text(
        'date,order_id,product,category,region,quantity,unit_price,total_amount\n'
        '"unterminated quote,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n'
    )

    with pytest.raises(ValueError, match="Could not parse CSV"):
        load_sales_data(str(csv_path))


def test_load_sales_data_missing_date_column(tmp_path):
    csv_path = tmp_path / "no_date.csv"
    csv_path.write_text(
        "order_id,product,category,region,quantity,unit_price,total_amount\n"
        "ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n"
    )

    with pytest.raises(ValueError, match="Could not parse CSV"):
        load_sales_data(str(csv_path))


def test_load_sales_data_non_csv_read_error(tmp_path):
    with pytest.raises(ValueError, match="Could not parse CSV"):
        load_sales_data(str(tmp_path))


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


def test_compute_monthly_trend():
    from data import compute_monthly_trend

    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10"]),
        "total_amount": [100.0, 50.0, 75.0],
    })

    result = compute_monthly_trend(df)

    assert list(result["total_sales"]) == [150.0, 75.0]
    assert result["month"].is_monotonic_increasing
