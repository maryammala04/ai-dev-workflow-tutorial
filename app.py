import streamlit as st
import plotly.express as px

from data import (
    compute_monthly_trend,
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)

DATA_PATH = "data/sales-data.csv"

COLOR_ACCENT = "#2C5F8A"    # trend line - the headline metric
COLOR_NEUTRAL = "#7C93A8"   # category + region bars - shared so both breakdowns read as one family

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
