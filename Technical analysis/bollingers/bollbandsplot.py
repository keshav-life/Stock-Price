import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf

# Fetch stock data
ticker = "BAJAJHLDNG.NS "
data = yf.download(ticker, period="2y")


# Calculate the 200-day moving average and standard deviation
data['MA200'] = data['Close'].rolling(window=200).mean()
data['STD200'] = data['Close'].rolling(window=200).std()

# Bollinger Bands with 1st, 2nd, and 3rd deviations
data['Upper1'] = data['MA200'] + data['STD200']
data['Lower1'] = data['MA200'] - data['STD200']
data['Upper2'] = data['MA200'] + (2 * data['STD200'])
data['Lower2'] = data['MA200'] - (2 * data['STD200'])
data['Upper3'] = data['MA200'] + (3 * data['STD200'])
data['Lower3'] = data['MA200'] - (3 * data['STD200'])

# Add custom space after the data for aesthetics
extra_dates = pd.date_range(start=data.index[-1], periods=60, freq='D')  # Add 30 extra days
data = data.reindex(data.index.union(extra_dates))  # Extend the index to add empty space

# Calculate the padding for the y-axis to increase the price range
price_min = data['Close'].min()
price_max = data['Close'].max()
padding = (price_max - price_min) * 0.35  # Add 10% padding above and below the price range
ymin = price_min - padding
ymax = price_max + padding

# Plot configurations
plots = [
    mpf.make_addplot(data['MA200'], color='blue', label='200 MA'),
    mpf.make_addplot(data['Upper1'], color='red', linestyle='--', label='Upper1'),
    mpf.make_addplot(data['Lower1'], color='red', linestyle='--', label='Lower1'),
    mpf.make_addplot(data['Upper2'], color='orange', linestyle='--', label='Upper2'),
    mpf.make_addplot(data['Lower2'], color='orange', linestyle='--', label='Lower2'),
    mpf.make_addplot(data['Upper3'], color='green', linestyle='--', label='Upper3'),
    mpf.make_addplot(data['Lower3'], color='green', linestyle='--', label='Lower3')
]

# Custom style for a black background and tighter grid spacing
my_style = mpf.make_mpf_style(
    base_mpf_style='nightclouds', 
    marketcolors=mpf.make_marketcolors(up='lime', down='red', wick={'up':'lime', 'down':'red'}, edge='inherit'),
    y_on_right=False,  # Price on left side
    gridstyle=":",  # Tighter grid lines (dotted)
    gridcolor='gray'  # Softer color for the grid
)

# Plot the candlestick chart with expanded y-axis range and additional space at the end
mpf.plot(data, type='candle', addplot=plots, 
         style=my_style, 
         title=f'{ticker} with Bollinger Bands (200 MA)', 
         ylabel='Price', 
         ylim=(ymin, ymax),  # Set y-axis limits with padding
         datetime_format='%b %d, %Y', 
         figsize=(12,8), 
         tight_layout=True,
         xrotation=0)  # No rotation for datetime on the x-axis
