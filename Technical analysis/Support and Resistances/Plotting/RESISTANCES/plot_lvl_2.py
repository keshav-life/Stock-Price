import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
import mplfinance as mpf  # For candlestick chart

# Fetch stock data for the past 2 years
def fetch_stock_data(symbol, days_offset=50):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)  # 2 years of data
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Function to mark support and resistance within each half-year section
def plot_support_resistance(stock_data, symbol, extra_days=50):
    # Determine half-year sections (4 sections for 2 years)
    half_year_periods = pd.date_range(stock_data.index.min(), stock_data.index.max(), freq='6M')

    # Extend time range by adding extra empty space at the end
    last_date = stock_data.index[-1]
    extended_dates = pd.date_range(last_date, last_date + timedelta(days=extra_days))
    extended_data = pd.DataFrame(index=extended_dates)
    stock_data = pd.concat([stock_data, extended_data])

    # Plot
    fig, ax = plt.subplots(figsize=(14, 8))
    mpf.plot(stock_data, type='candle', ax=ax, style='charles', show_nontrading=True)

    # Plot support and resistance for each half-year section
    for i in range(len(half_year_periods) - 1):
        period_data = stock_data.loc[half_year_periods[i]:half_year_periods[i + 1]]
        if not period_data.empty:
            highest_price = period_data['High'].max()
            lowest_price = period_data['Low'].min()

            # Mark resistance and support within each section
            ax.hlines(y=highest_price, xmin=half_year_periods[i], xmax=half_year_periods[i + 1],
                       color='red', linestyle='--', linewidth=1.5, label=f'Resistance {i+1}: {highest_price:.2f}')
            ax.hlines(y=lowest_price, xmin=half_year_periods[i], xmax=half_year_periods[i + 1],
                       color='green', linestyle='--', linewidth=1.5, label=f'Support {i+1}: {lowest_price:.2f}')

    # Ensure support and resistance for the latest half-year period is added
    latest_period_data = stock_data.loc[half_year_periods[-1]:]
    if not latest_period_data.empty:
        highest_price_latest = latest_period_data['High'].max()
        lowest_price_latest = latest_period_data['Low'].min()
        ax.hlines(y=highest_price_latest, xmin=half_year_periods[-1], xmax=stock_data.index.max(),
                   color='red', linestyle='--', linewidth=1.5, label=f'Resistance Latest: {highest_price_latest:.2f}')
        ax.hlines(y=lowest_price_latest, xmin=half_year_periods[-1], xmax=stock_data.index.max(),
                   color='green', linestyle='--', linewidth=1.5, label=f'Support Latest: {lowest_price_latest:.2f}')

    # Customize chart appearance (background, grid, spacing, etc.)
    ax.set_facecolor('#000000')  # Black background
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)

    # Shrink grid spacing
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

    # Add padding at the end of the chart for better visualization
    ax.set_xlim(stock_data.index.min(), stock_data.index.max())

    # Title and labels
    ax.set_title(f"{symbol} Stock - Support and Resistance Levels", color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Price (USD)", color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Show plot
    plt.tight_layout()
    plt.show()

# Example usage
symbol = 'AAPL'  # Replace with your stock symbol
stock_data = fetch_stock_data(symbol)
plot_support_resistance(stock_data, symbol)
