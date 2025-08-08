import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Stock Correlation Analysis")

tickers = st.text_input("Enter ticker symbols separated by commas", "AAPL, MSFT, GOOG")
tickers = [t.strip().upper() for t in tickers.split(",")]

start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2024-01-01"))

if start_date >= end_date:
    st.error("End date must be after start date")
else:
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
    st.write("Raw closing prices:")
    st.dataframe(data.tail())

    cumulative_returns = (1 + data.pct_change().dropna()).cumprod()

    st.line_chart(cumulative_returns)
