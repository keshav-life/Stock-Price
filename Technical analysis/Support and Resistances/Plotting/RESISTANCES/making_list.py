import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Name of the stock
ticker = 'AMBER.NS'
data = yf.download(ticker, start='2022-01-01', end='2024-01-01')

# datetime time index
data.index = pd.to_datetime(data.index)

# My parameters for resistance 
lookback_period = 20  # days to check for no higher price
drop_threshold = 0.15  # check for price drop of at least 15%

# DataFrame to store resistance levels
resistance_df = pd.DataFrame(columns=['Date', 'Resistance Level'])

# Array for resistance levels to be used in chart plotting
resistance_levels = []

# Finding resistance levels
for i in range(lookback_period, len(data)):
    # Check if it's a new high in the last 20 days
    if data['High'][i] > data['High'][i - lookback_period:i].max():
        drop_price = data['High'][i] * (1 - drop_threshold)  # Calculate the price drop level (15%)

        # Check if the price drops within the threshold in the next 15 days
        if any(data['Low'][i + 1:i + 16] < drop_price):
            # Ensure no higher price in the past 20 days before this new high
            if all(data['High'][i - lookback_period:i] <= data['High'][i]):
                resistance_levels.append((data.index[i], data['High'][i]))  # Store date and price
                resistance_df = resistance_df.append({'Date': data.index[i], 'Resistance Level': data['High'][i]}, ignore_index=True)

# To find the latest highest point after which the price has never gone up (one more added condition)
latest_high = None
latest_high_date = None
for i in range(lookback_period, len(data)):
    if data['High'][i] > data['High'][i - lookback_period:i].max():  # New high
        if latest_high is None or data['High'][i] > latest_high:  # Check for latest high
            if all(data['High'][i - lookback_period:i] <= data['High'][i]):  # Ensure no higher price in the past 20 days
                latest_high = data['High'][i]
                latest_high_date = data.index[i]

# Mark resistance levels on the chart by stretching lines across the entire chart
resistance_lines = []
for date, price in resistance_levels:
    resistance_lines.append(mpf.make_addplot([price] * len(data), color='red', linestyle='--', width=1))

# Mark the latest highest point if found
if latest_high is not None:
    resistance_lines.append(mpf.make_addplot([latest_high] * len(data), color='blue', linestyle='--', width=1))

# Plotting with mplfinance
mpf.plot(data,
         type='candle',
         style='charles',
         title=f"{ticker} Stock Price with Resistance Levels",
         ylabel='Price',
         ylabel_lower='',
         addplot=resistance_lines,
         datetime_format='%Y-%m-%d',
         xrotation=45)

# Display the resistance levels in a tabular format
print(resistance_df)
