import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# =============================================================================
#                               Input data
# =============================================================================
#Initial inputs - input set(!!!) of tickers in the corresponding list
#Change data in start/end variable as you wish

tickers = ['AAPL']
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

# Download data in accordance to ticker, start and end date
stocks = pd.DataFrame(yf.download(tickers, start, end)['Adj Close'])
stocks.columns = tickers

# =============================================================================
#                               MACD function
# =============================================================================
def macd(data, per1, per2, per3):
    macd_df = pd.DataFrame()
    
    for ticker in tickers:
        # Calculating EMA_per1
        macd_df['mod_price1'] = data[ticker]
        macd_df['mod_price1'][0:per1] = (macd_df['mod_price1'].
                                              rolling(per1).
                                              mean())[0:per1]
        macd_df['EMA1'] = macd_df['mod_price1'].ewm(span=per1,
                                                    adjust=False).mean()
        
        # Calculating EMA_per2
        macd_df["mod_price2"] = data[ticker]
        macd_df["mod_price2"][0:per2] = (macd_df["mod_price2"].rolling(per2).
                                             mean())[0:per2]
        macd_df['EMA2'] = macd_df['mod_price2'].ewm(per2, adjust=False).mean()
        
        # Calculating MACD line
        macd_df[ticker] = macd_df["EMA1"] - macd_df["EMA2"]
        
        # Calculating signal line
        macd_df['{} Sig'.format(ticker)] = (macd_df[ticker].
                                            ewm(per3, adjust=False).mean())
        
        # Graphical interpretation of MACD
        macd_df[ticker].plot(kind='line',
                             color='blue',
                             label='MACD line')
        macd_df['{} Sig'.format(ticker)].plot(kind='line',
                                              color='red',
                                              label='Signal')
        plt.title(ticker)
        plt.plot([start, end],
                 [0, 0],
                 color='black')
        plt.legend()
        plt.show()
        
        
    return macd_df[tickers]

# Now you can simply call 'your DataFrame for MACD' = macd(data, period)
# and you will get one DataFrame with MACD values for different stocks

macd_table = macd(stocks, 12, 26, 9)


# You can also try to find MACD for all s&p500 tickers. Refer to the method
# in my RSI_function file in the same repository (finance_functions)

# Enjoy it!


# contacts: george.druzhkin@gmail.com
# https://github.com/george-druzhkin/finance_functions