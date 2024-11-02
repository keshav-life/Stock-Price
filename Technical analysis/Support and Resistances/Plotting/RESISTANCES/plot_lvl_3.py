'''import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Download stock data (use any ticker for testing)
ticker = 'APARINDS.NS'
data = yf.download(ticker, start='2022-01-01', end='2024-01-01')

# Ensure the index is datetime for proper plotting
data.index = pd.to_datetime(data.index)

# Parameters for resistance level identification
lookback_period = 20  # days to check for no higher price
drop_thresholds = (0.15, 0.12)  # check for price drops between 15% and 12%

# Find resistance levels
resistance_levels = []
for i in range(lookback_period, len(data)):
    if data['High'][i] > data['High'][i-lookback_period:i].max():  # Check if it's a new high in the last 20 days
        drop_price_15 = data['High'][i] * (1 - drop_thresholds[0])  # Calculate the price drop level (15%)
        drop_price_12 = data['High'][i] * (1 - drop_thresholds[1])  # Calculate the price drop level (12%)
        
        # Check if price drops within the thresholds in the next 15 days
        if any(data['Low'][i+1:i+16] < drop_price_15) or any(data['Low'][i+1:i+16] < drop_price_12):
            resistance_levels.append((data.index[i], data['High'][i]))  # Store date and price

# Find the latest highest point after which price has never gone up
latest_high = None
latest_high_date = None
for i in range(lookback_period, len(data)):
    if data['High'][i] > data['High'][i-lookback_period:i].max():  # New high
        if latest_high is None or data['High'][i] > latest_high:  # Check for latest high
            if all(data['High'][i-lookback_period:i] <= data['High'][i]):  # Ensure no higher price in the past 20 days
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
'''

import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Name of the stock
ticker = ' AMBER.NS '
data = yf.download(ticker, start='2022-01-01', end='2024-01-01')

# datetime time index
data.index = pd.to_datetime(data.index)

# My parameters for resistance 
lookback_period = 20  # days to check for no higher pricer
drop_threshold = 0.15  # check for price drop of at least 15%

# array for resistance levels
resistance_levels = []
for i in range(lookback_period, len(data)):
    # Check if it's a new high in the last 20 days
    if data['High'][i] > data['High'][i - lookback_period:i].max():
        drop_price = data['High'][i] * (1 - drop_threshold)  # Calculate the price drop level (15%)

        # Check if the price drops within the threshold in the next 15 days
        if any(data['Low'][i + 1:i + 16] < drop_price):
            # Ensure no higher price in the past 20 days before this new high
            if all(data['High'][i - lookback_period:i] <= data['High'][i]):
                resistance_levels.append((data.index[i], data['High'][i]))  # Store date and price

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
