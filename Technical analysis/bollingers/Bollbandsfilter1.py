"""This strategy will be based on to find whether the stock price is between 2 and 3rd deviation on either side, it will just tell now here, and not make a list of it"""

import yfinance as yf
import pandas as pd
import numpy as np

# List of stocks to check
stocks = ['AJANTPHARM.NS', ]  # Add more stock symbols as needed

def is_between(stock):
    # Fetch stock data
    data = yf.download(stock, period='2y')

    # Calculate the 200-day moving average and standard deviations
    data['MA200'] = data['Close'].rolling(window=200).mean()
    data['STD200'] = data['Close'].rolling(window=200).std()

    # Bollinger Bands with 2nd and 3rd deviations
    data['Upper2'] = data['MA200'] + (2 * data['STD200'])
    data['Lower2'] = data['MA200'] - (2 * data['STD200'])
    data['Upper3'] = data['MA200'] + (3 * data['STD200'])
    data['Lower3'] = data['MA200'] - (3 * data['STD200'])

    # Get the most recent price
    latest_price = data['Close'][-1]

    # Check if the price is between the 2nd and 3rd deviation on the upper or lower side
    if data['Lower3'][-1] < latest_price < data['Lower2'][-1]:
        return f"{stock}: Price is between the 2nd and 3rd lower deviation."
    elif data['Upper2'][-1] < latest_price < data['Upper3'][-1]:
        return f"{stock}: Price is between the 2nd and 3rd upper deviation."
    else:
        return f"{stock}: Price is not between the 2nd and 3rd deviation."

# Check for all stocks in the list
results = [is_between(stock) for stock in stocks]

# Display the results
for result in results:
    print(result)
