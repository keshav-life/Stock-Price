# List of stocks to check
stock_nifty = pd.read_csv("C:/Users/91705/Documents/Arsenal TECH/AI and CS/minor project/Technical analysis/bollingers/nifty_500list.csv")
symbol = stock_nifty['Symbol']
stocks = symbol.head(20) #to take first 20 symbols
