import streamlit as st

from data import (
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)

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

total_sales = compute_total_sales(df)
total_orders = compute_total_orders(df)

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
