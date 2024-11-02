import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta

# Fetch stock data for the past 2 years
def fetch_stock_data(symbol, days_offset=50):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)  # 2 years of data
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Plotting function
def plot_support_resistance(stock_data, symbol, extra_days=50):
    # Determine the highest (resistance) and lowest (support) points
    highest_price = stock_data['High'].max()
    lowest_price = stock_data['Low'].min()

    # Extend time range by adding extra empty space at the end
    last_date = stock_data.index[-1]
    extended_dates = pd.date_range(last_date, last_date + timedelta(days=extra_days))
    extended_data = pd.DataFrame(index=extended_dates)
    stock_data = pd.concat([stock_data, extended_data])

    # Plot
    plt.figure(figsize=(14, 8))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')

    # Mark resistance (highest) and support (lowest) levels
    plt.axhline(y=highest_price, color='red', linestyle='--', label=f'Resistance: {highest_price:.2f}')
    plt.axhline(y=lowest_price, color='green', linestyle='--', label=f'Support: {lowest_price:.2f}')

    # Customize chart appearance (background, grid, spacing, etc.)
    plt.gca().set_facecolor('#f0f0f0')  # Light background color
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Adding some padding at the end of the chart for better visualization
    plt.xlim(stock_data.index.min(), stock_data.index.max())

    # Title and labels
    plt.title(f"{symbol} Stock - Support and Resistance Levels")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()

# Example usage
symbol = 'AAPL'  # Replace with your stock symbol
stock_data = fetch_stock_data(symbol)
plot_support_resistance(stock_data, symbol)
