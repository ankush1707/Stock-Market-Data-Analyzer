"""Optional dashboard:  streamlit run app.py"""
from datetime import date, timedelta
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import get_stock_data
from src.cleaning import clean_data
from src.analysis import add_indicators, summarize, risk_label

st.set_page_config(page_title="Stock Market Data Analyzer", layout="wide")
st.title("Stock Market Data Analyzer")

ticker = st.sidebar.text_input("Ticker", "AAPL").upper()
start = st.sidebar.date_input("Start", date.today() - timedelta(days=730))
end = st.sidebar.date_input("End", date.today())
short = st.sidebar.slider("Short MA", 5, 50, 20)
long = st.sidebar.slider("Long MA", 30, 200, 50)
upload = st.sidebar.file_uploader("...or upload CSV", type="csv")


@st.cache_data(show_spinner=True)
def load(ticker, start, end):
    raw, src = get_stock_data(ticker, str(start), str(end))
    return clean_data(raw, str(start), str(end)), src


if upload is not None:
    import pandas as pd
    df, source = clean_data(pd.read_csv(upload)), "Uploaded CSV"
else:
    df, source = load(ticker, start, end)

df = add_indicators(df, short, long)
s = summarize(df)
st.caption(f"Source: {source}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total return", f"{s['total_return']:.1%}")
c2.metric("Volatility (ann.)", f"{s['annualized_volatility']:.1%}", risk_label(s["annualized_volatility"]))
c3.metric("Max drawdown", f"{s['max_drawdown']:.1%}")
c4.metric("Trend", s["current_trend"])

fig = go.Figure()
fig.add_scatter(x=df.index, y=df["Close"], name="Close")
fig.add_scatter(x=df.index, y=df[f"SMA_{short}"], name=f"SMA {short}")
fig.add_scatter(x=df.index, y=df[f"SMA_{long}"], name=f"SMA {long}")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
left.subheader("Daily return distribution")
left.plotly_chart(go.Figure(go.Histogram(x=df["Daily_Return"].dropna(), nbinsx=50)),
                  use_container_width=True)
right.subheader("20-day rolling volatility")
right.line_chart(df["Volatility_20"])
st.dataframe(df.tail(30))
