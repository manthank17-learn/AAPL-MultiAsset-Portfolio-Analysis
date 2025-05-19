import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Define tickers and date range ===
tickers = ['AAPL', 'MSFT', 'GOOG']
start_date = '2023-01-01'
end_date = '2024-01-01'

# === 2. Download only daily closing prices ===
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']

# === 3. Save raw price data ===
data.to_csv("data/multi_stock_prices.csv")

# === 4. Compute daily % returns ===
daily_returns = data.pct_change().dropna()

# === 5. Compute cumulative returns ===
cumulative_returns = (1 + daily_returns).cumprod()

# === 6. Plot cumulative returns ===
plt.figure(figsize=(14, 6))
for ticker in tickers:
    plt.plot(cumulative_returns[ticker], label=ticker)
plt.title('Cumulative Returns (2023)')
plt.xlabel('Date')
plt.ylabel('Growth of ₹1 Investment')
plt.grid(True)
plt.legend()
plt.savefig("plots/multi_cumulative_returns.png")
plt.show()

# === 7. Correlation heatmap of daily returns ===
plt.figure(figsize=(8, 6))
sns.heatmap(daily_returns.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title('Correlation Matrix of Daily Returns')
plt.savefig("plots/correlation_matrix.png")
plt.show()
# === 8. Portfolio Simulation ===

# Set portfolio weights: AAPL=40%, MSFT=30%, GOOG=30%
weights = [0.4, 0.3, 0.3]
initial_investment = 10_000  # ₹10,000

# Calculate weighted daily returns
weighted_returns = (daily_returns * weights).sum(axis=1)

# Cumulative portfolio value
portfolio_value = (1 + weighted_returns).cumprod() * initial_investment

# Save to CSV
portfolio_value.to_csv("data/portfolio_value.csv")

# Plot portfolio performance
plt.figure(figsize=(14, 5))
plt.plot(portfolio_value, label='Portfolio Value (₹)')
plt.title("Portfolio Growth (₹10,000 Investment)")
plt.xlabel("Date")
plt.ylabel("Value (₹)")
plt.grid(True)
plt.legend()
plt.savefig("plots/portfolio_growth.png")
plt.show()
