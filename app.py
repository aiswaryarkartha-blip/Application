import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Yahoo Finance Stock Dashboard")

ticker = st.text_input(
    "Enter Stock Symbol",
    value="AAPL"
).upper()

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max"
    ],
    index=1
)

interval_map = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "max": "1mo"
}

interval = interval_map[period]

try:
    data = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        st.error("No data found.")
        st.stop()

    st.subheader(f"{ticker} Stock Price")

    fig = px.line(
        data,
        x=data.index,
        y="Close",
        title=f"{ticker} Closing Price ({period})"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Latest Data")

    st.dataframe(
        data.tail(),
        use_container_width=True
    )

except Exception as e:
    st.error(e)
