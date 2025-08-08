import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Stock Correlation & Portfolio Analysis")

# === Inputs ===
tickers = st.text_input("Enter ticker symbols separated by commas", "AAPL, MSFT, GOOG")
tickers = [t.strip().upper() for t in tickers.split(",")]

start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2024-01-01"))

if start_date >= end_date:
    st.error("End date must be after start date")
else:
    # Download closing price data
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
    st.subheader("Raw closing prices (last 5 rows)")
    st.dataframe(data.tail())

    # Calculate daily and cumulative returns
    daily_returns = data.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod()

    # Plot cumulative returns
    st.subheader("Cumulative Returns")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    for ticker in tickers:
        ax1.plot(cumulative_returns[ticker], label=ticker)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Growth of ₹1 Investment")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Correlation heatmap
    st.subheader("Correlation Matrix of Daily Returns")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(daily_returns.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
    st.pyplot(fig2)

    # Portfolio simulation inputs
    st.subheader("Portfolio Simulation")
    weights_input = st.text_input(
        "Portfolio weights (comma-separated, sum to 1)", "0.4, 0.3, 0.3"
    )

    try:
        weights = [float(w.strip()) for w in weights_input.split(",")]
        if len(weights) != len(tickers):
            st.error("Number of weights must match number of tickers")
        elif abs(sum(weights) - 1) > 1e-6:
            st.error("Weights must sum to 1")
        else:
            initial_investment = st.number_input(
                "Initial investment (₹)", value=10000, step=1000
            )

            weighted_returns = (daily_returns * weights).sum(axis=1)
            portfolio_value = (1 + weighted_returns).cumprod() * initial_investment

            # Plot portfolio growth
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            ax3.plot(portfolio_value, label="Portfolio Value (₹)")
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Value (₹)")
            ax3.grid(True)
            ax3.legend()
            st.pyplot(fig3)

            # Summary
            st.markdown("### Summary")
            st.write(f"Date range: {start_date} to {end_date}")
            st.write(f"Number of tickers: {len(tickers)}")
            avg_return = daily_returns.mean().mean() * 100
            total_growth = (portfolio_value.iloc[-1] / initial_investment - 1) * 100
            st.write(f"Average daily return across portfolio: {avg_return:.2f}%")
            st.write(f"Total portfolio growth: {total_growth:.2f}%")

            # Download buttons
            csv_data = data.to_csv().encode('utf-8')
            st.download_button(
                label="Download raw price data as CSV",
                data=csv_data,
                file_name='stock_prices.csv',
                mime='text/csv'
            )

            csv_portfolio = portfolio_value.to_csv().encode('utf-8')
            st.download_button(
                label="Download portfolio value as CSV",
                data=csv_portfolio,
                file_name='portfolio_value.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"Invalid weights input: {e}")
