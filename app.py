import sys
from pathlib import Path

import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import apply_theme

st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide",
)
apply_theme()

_BASE = Path(__file__).resolve().parent
DATA_PATH = next(
    (p for p in (_BASE / "stocks_cleaned.csv", _BASE / "stocks_cleaned.csv.gz") if p.exists()),
    _BASE / "stocks_cleaned.csv",
)


@st.cache_data(show_spinner="Loading stock data...")
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    if "year" not in data.columns:
        data["year"] = data["date"].dt.year
    if "daily_return" not in data.columns and {"Name", "close"}.issubset(data.columns):
        data = data.sort_values(["Name", "date"])
        previous_close = data.groupby("Name")["close"].shift(1)
        data["daily_return"] = (
            (data["close"] - previous_close) / previous_close
        ) * 100
    return data


st.title("📈 Stock Market Analysis")
st.subheader("Explore historical stock prices, returns, trading volume, and volatility.")

if not DATA_PATH.exists():
    st.error("The data file was not found.")
    st.info(
        "Place your `stocks_cleaned.csv` file in the same folder as `app.py`, "
        "then run the app again."
    )
    st.stop()

df = load_data(str(DATA_PATH))

st.markdown(
    """
    This project analyzes historical US stock market data from 2013 to 2018.
    It includes data cleaning, feature engineering, exploratory data analysis,
    and interactive stock exploration.
    """
)

col1, col2, col3 = st.columns(3)
col1.metric("Total records", f"{len(df):,}")
col2.metric("Number of stocks", f"{df['Name'].nunique():,}")
if "date" in df.columns and df["date"].notna().any():
    col3.metric(
        "Date range",
        f"{df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}",
    )

st.divider()
st.subheader("What's inside?")
left, right = st.columns(2)
with left:
    st.markdown(
        """
        **Market Analysis**
        - Annual average daily returns
        - Annual return volatility
        - Highest average trading volume
        - Positive vs. negative return days
        """
    )
with right:
    st.markdown(
        """
        **Stock Explorer**
        - Select an individual stock
        - Filter by date range
        - Explore closing prices, volume, and daily returns
        """
    )

st.caption("Use the pages in the sidebar to navigate through the analysis.")
