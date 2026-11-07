import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Stock Explorer", page_icon="🔎", layout="wide")
DATA_PATH = Path(__file__).resolve().parents[1] / "stocks_cleaned.csv"


@st.cache_data(show_spinner="Loading stock data...")
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    if "daily_return" not in data.columns:
        data = data.sort_values(["Name", "date"])
        previous_close = data.groupby("Name")["close"].shift(1)
        data["daily_return"] = ((data["close"] - previous_close) / previous_close) * 100
    return data


st.title("🔎 Stock Explorer")
if not DATA_PATH.exists():
    st.error("stocks_cleaned.csv was not found. Put it beside app.py.")
    st.stop()

df = load_data(str(DATA_PATH))
symbols = sorted(df["Name"].dropna().unique().tolist())
selected_stock = st.selectbox("Choose a stock", symbols)

stock = df[df["Name"] == selected_stock].sort_values("date").copy()
if stock.empty:
    st.warning("No records were found for this stock.")
    st.stop()

min_date = stock["date"].min().date()
max_date = stock["date"].max().date()

date_range = st.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    stock = stock[
        (stock["date"].dt.date >= start_date) &
        (stock["date"].dt.date <= end_date)
    ]

if stock.empty:
    st.warning("No data is available for the selected date range.")
    st.stop()

latest = stock.iloc[-1]
first = stock.iloc[0]
a, b, c = st.columns(3)
a.metric("Latest closing price", f"${latest['close']:.2f}")
b.metric("Average daily return", f"{stock['daily_return'].mean():.3f}%")
c.metric("Average trading volume", f"{stock['volume'].mean():,.0f}")

st.subheader(f"{selected_stock} closing price over time")
fig_price = px.line(stock, x="date", y="close", title="Closing Price")
st.plotly_chart(fig_price, use_container_width=True)

st.subheader("Trading volume over time")
fig_volume = px.line(stock, x="date", y="volume", title="Trading Volume")
st.plotly_chart(fig_volume, use_container_width=True)

st.subheader("Daily returns")
fig_returns = px.line(
    stock, x="date", y="daily_return", title="Daily Return (%)"
)
st.plotly_chart(fig_returns, use_container_width=True)

with st.expander("View filtered data"):
    st.dataframe(
        stock[["date", "Name", "open", "high", "low", "close", "volume", "daily_return"]],
        use_container_width=True,
        hide_index=True,
    )
