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
