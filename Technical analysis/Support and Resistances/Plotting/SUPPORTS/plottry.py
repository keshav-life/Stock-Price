import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Name of the stock
ticker = 'AMBER.NS'
data = yf.download(ticker, start='2022-01-01', end='2024-01-01')

# datetime time index
data.index = pd.to_datetime(data.index)

# My parameters for support 
lookback_period_support = 30  # days to check for no lower price before the support point
rise_threshold = 0.15  # check for price rise of at least 15% after touching support

# array for support levels
support_levels = []
for i in range(lookback_period_support, len(data)):
    # Check if it's a new low in the last 30 days
    if data['Low'][i] < data['Low'][i - lookback_period_support:i].min():
        rise_price = data['Low'][i] * (1 + rise_threshold)  # Calculate the price rise level (15%)

        # Check if the price rises within the threshold in the next 15 days
        if any(data['High'][i + 1:i + 16] > rise_price):
            # Ensure no lower price in the past 30 days before this new low
            if all(data['Low'][i - lookback_period_support:i] >= data['Low'][i]):
                support_levels.append((data.index[i], data['Low'][i]))  # Store date and price

# To find the latest lowest point after which the price has never dropped
latest_low = None
latest_low_date = None
for i in range(lookback_period_support, len(data)):
    if data['Low'][i] < data['Low'][i - lookback_period_support:i].min():  # New low
        if latest_low is None or data['Low'][i] < latest_low:  # Check for latest low
            if all(data['Low'][i - lookback_period_support:i] >= data['Low'][i]):  # Ensure no lower price in the past 30 days
                latest_low = data['Low'][i]
                latest_low_date = data.index[i]

# Mark support levels on the chart by stretching lines across the entire chart
support_lines = []
for date, price in support_levels:
    support_lines.append(mpf.make_addplot([price] * len(data), color='green', linestyle='--', width=1))

# Mark the latest lowest point if found
if latest_low is not None:
    support_lines.append(mpf.make_addplot([latest_low] * len(data), color='blue', linestyle='--', width=1))

# Plotting with mplfinance
mpf.plot(data,
         type='candle',
         style='charles',
         title=f"{ticker} Stock Price with Support Levels",
         ylabel='Price',
         ylabel_lower='',
         addplot=support_lines,
         datetime_format='%Y-%m-%d',
         xrotation=45)
