import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Yahoo Finance Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Yahoo Finance Stock Dashboard")

st.write("Enter any stock ticker (Example: AAPL, MSFT, TSLA, RELIANCE.NS, TCS.NS)")

# ----------------------------
# Sidebar
# ----------------------------
ticker = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL"
).strip().upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    (
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    )
)

interval_mapping = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "10y": "1mo",
    "max": "1mo"
}

interval = interval_mapping[period]

# ----------------------------
# Download Data
# ----------------------------
with st.spinner("Fetching data from Yahoo Finance..."):

    try:

        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            threads=False
        )

        # Fix MultiIndex columns (new yfinance versions)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if data.empty:
            st.error("No data found. Please check the ticker symbol.")
            st.stop()

        if "Close" not in data.columns:
            st.error("Closing price not available.")
            st.stop()

    except Exception as e:
        st.error(f"Error downloading data:\n\n{e}")
        st.stop()

# ----------------------------
# Metrics
# ----------------------------

latest_price = float(data["Close"].iloc[-1])
first_price = float(data["Close"].iloc[0])

change = latest_price - first_price
pct_change = (change / first_price) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Latest Price", f"${latest_price:,.2f}")
col2.metric("Change", f"{change:,.2f}")
col3.metric("% Change", f"{pct_change:.2f}%")

# ----------------------------
# Line Chart
# ----------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Close Price",
        line=dict(width=2)
    )
)

fig.update_layout(
    title=f"{ticker} Closing Price ({period})",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Data Table
# ----------------------------

st.subheader("Historical Data")

display_df = data.copy()

display_df.reset_index(inplace=True)

st.dataframe(
    display_df,
    use_container_width=True
)

# ----------------------------
# Download CSV
# ----------------------------

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"{ticker}_{period}.csv",
    mime="text/csv"
)

# ----------------------------
# Footer
# ----------------------------

st.caption("Data Source: Yahoo Finance")
