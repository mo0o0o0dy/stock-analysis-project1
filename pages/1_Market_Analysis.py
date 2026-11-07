import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import apply_theme, style_fig, PALETTE, TEAL, GOLD, DIRECTION_COLORS

st.write("BASE:", str(_BASE))
st.write("FILES:", sorted(p.name for p in _BASE.iterdir()))

st.set_page_config(page_title="Market Analysis", page_icon="📊", layout="wide")
apply_theme()
DATA_PATH = Path(__file__).resolve().parents[1] / "stocks_cleaned.csv"


@st.cache_data(show_spinner="Loading stock data...")
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    if "year" not in data.columns:
        data["year"] = data["date"].dt.year
    if "daily_return" not in data.columns:
        data = data.sort_values(["Name", "date"])
        previous_close = data.groupby("Name")["close"].shift(1)
        data["daily_return"] = ((data["close"] - previous_close) / previous_close) * 100
    return data


st.title("📊 Market Analysis")
if not DATA_PATH.exists():
    st.error("stocks_cleaned.csv was not found. Put it beside app.py.")
    st.stop()

df = load_data(str(DATA_PATH))
required = {"Name", "date", "close", "volume", "daily_return", "year"}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(sorted(missing))}")
    st.stop()

st.markdown("Explore the main findings from the exploratory data analysis.")

# Annual metrics
yearly_returns = df.groupby("year")["daily_return"].mean()
yearly_volatility = df.groupby("year")["daily_return"].std()

c1, c2 = st.columns(2)
if not yearly_volatility.dropna().empty:
    most_volatile = yearly_volatility.idxmax()
    most_stable = yearly_volatility.idxmin()
    c1.metric("Most volatile year", str(int(most_volatile)),
              f"{yearly_volatility.max():.3f}% standard deviation")
    c2.metric("Most stable year", str(int(most_stable)),
              f"{yearly_volatility.min():.3f}% standard deviation")

st.subheader("Annual average daily returns")
returns_chart = yearly_returns.rename("Average daily return (%)").reset_index()
fig_returns = px.line(
    returns_chart, x="year", y="Average daily return (%)",
    markers=True, title="Average Daily Stock Returns by Year",
    color_discrete_sequence=[TEAL],
)
fig_returns.update_traces(line=dict(width=3), marker=dict(size=9))
fig_returns.update_xaxes(dtick=1)
st.plotly_chart(style_fig(fig_returns), use_container_width=True)

st.subheader("Annual stock return volatility")
vol_chart = yearly_volatility.rename("Standard deviation (%)").reset_index()
fig_vol = px.line(
    vol_chart, x="year", y="Standard deviation (%)",
    markers=True, title="Annual Stock Return Volatility",
    color_discrete_sequence=[GOLD],
)
fig_vol.update_traces(line=dict(width=3), marker=dict(size=9))
fig_vol.update_xaxes(dtick=1)
st.plotly_chart(style_fig(fig_vol), use_container_width=True)

st.caption(
    "Note: 2013 and 2018 are partial years in this dataset, so comparisons "
    "involving those years should be interpreted carefully."
)

# Top stocks
st.subheader("Stocks with the highest average daily returns")
avg_returns = df.groupby("Name")["daily_return"].mean().dropna()
top_returns = avg_returns.sort_values(ascending=False).head(10)
ret_chart = top_returns.rename("Average daily return (%)").reset_index()
fig_top_returns = px.bar(
    ret_chart, x="Name", y="Average daily return (%)",
    title="Top 10 Stocks by Average Daily Return",
    color_discrete_sequence=[TEAL],
)
fig_top_returns.update_traces(marker_line_width=0)
st.plotly_chart(style_fig(fig_top_returns), use_container_width=True)

st.subheader("Stocks with the highest average trading volume")
avg_volume = df.groupby("Name")["volume"].mean().dropna()
top_volume = avg_volume.sort_values(ascending=False).head(10)
volume_chart = top_volume.rename("Average trading volume").reset_index()
fig_volume = px.bar(
    volume_chart, x="Name", y="Average trading volume",
    title="Top 10 Stocks by Average Trading Volume",
    color_discrete_sequence=[PALETTE[2]],
)
fig_volume.update_traces(marker_line_width=0)
st.plotly_chart(style_fig(fig_volume), use_container_width=True)

st.subheader("Positive and negative daily returns")
directions = pd.Series({
    "Positive": int((df["daily_return"] > 0).sum()),
    "Negative": int((df["daily_return"] < 0).sum()),
    "Zero": int((df["daily_return"] == 0).sum()),
}).rename_axis("Return direction").reset_index(name="Number of observations")
fig_pie = px.pie(
    directions, names="Return direction", values="Number of observations",
    title="Distribution of Positive, Negative, and Zero Daily Returns",
    color="Return direction", color_discrete_map=DIRECTION_COLORS, hole=0.55,
)
fig_pie.update_traces(textinfo="percent+label",
                      marker=dict(line=dict(color="#0B1020", width=3)))
st.plotly_chart(style_fig(fig_pie, height=460), use_container_width=True)

st.subheader("Trading volume vs. daily return")
sample = df[["volume", "daily_return"]].dropna()
if len(sample) > 5000:
    sample = sample.sample(5000, random_state=42)
correlation = sample["volume"].corr(sample["daily_return"])
st.metric("Pearson correlation (sample of up to 5,000 records)", f"{correlation:.4f}")
fig_scatter = px.scatter(
    sample, x="volume", y="daily_return",
    opacity=0.35, title="Trading Volume vs. Daily Returns (sample)",
    color_discrete_sequence=[PALETTE[3]],
)
fig_scatter.update_traces(marker=dict(size=6))
st.plotly_chart(style_fig(fig_scatter, height=460), use_container_width=True)
st.caption(
    "A correlation close to zero indicates little linear association in this sample; "
    "it does not prove that no relationship of any kind exists."
)
