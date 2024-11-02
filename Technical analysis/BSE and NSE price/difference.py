'''import pandas as pd 
import yfinance as yf 

stock_nse = 'AJANTPHARM.NS'
stock_bse = 'AJANTPHARM.BO'
data_nse = yf.download('stock_nse', period='2d')
data_bse = yf.download('stock_bse', period='2d')

print("NSE Data:\n", data_nse)
print("NSE Data:\n", data_bse)
'''

import yfinance as yf


ticker_nse = yf.Ticker("AJANTPHARM.NS")
ticker_bse = yf.Ticker("AJANTPHARM.BO")

# Update the access method for Close prices
current_price_nse = ticker_nse.history(period="1d")['Close'].iloc[0]
current_price_bse = ticker_bse.history(period="1d")['Close'].iloc[0]

