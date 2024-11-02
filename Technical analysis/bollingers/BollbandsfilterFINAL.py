import pandas as pd
import yfinance as yf
from tabulate import tabulate

# here I load the list of Nifty 500 stocks from the CSV file
file_path = "C:/Users/91705/Documents/Arsenal TECH/AI and CS/minor project/Technical analysis/bollingers/nifty_500list.csv"
stock_nifty = pd.read_csv(file_path)
stocks = [f"{symbol}.NS" for symbol in stock_nifty['Symbol'].head(100).tolist()]

def get_bollinger_bands(symbol):
    data = yf.download(symbol, period='1y', interval='1d')
    if data.empty:
        return {
            'Symbol': symbol,
            'Latest Close': None,
            'Upper Band 2': None,
            'Upper Band 3': None,
            'Is Between 2nd and 3rd': None,
            'Error': 'No data found'
        }

    data['MA200'] = data['Close'].rolling(window=200).mean()
    data['STD'] = data['Close'].rolling(window=200).std()
    upper_band_2 = data['MA200'].iloc[-1] + (data['STD'].iloc[-1] * 2)
    upper_band_3 = data['MA200'].iloc[-1] + (data['STD'].iloc[-1] * 3)
    latest_close = data['Close'].iloc[-1]
    
    is_between = upper_band_2 < latest_close < upper_band_3
    return {
        'Symbol': symbol,
        'Latest Close': latest_close,
        'Upper Band 2': upper_band_2,
        'Upper Band 3': upper_band_3,
        'Is Between 2nd and 3rd': is_between,
        'Error': None
    }

results = [get_bollinger_bands(stock) for stock in stocks]
results_df = pd.DataFrame(results)
qualifying_stocks_df = results_df[results_df['Is Between 2nd and 3rd'] == True]

# Print the results in a tabular format
print(tabulate(qualifying_stocks_df, headers='keys', tablefmt='psql'))
