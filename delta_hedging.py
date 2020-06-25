import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import math

start = dt.date(2020,6,11)
end = dt.date(2020,6,26)
option_ticker  = 'MSFT200626P00200000'
option_strike = 200
option_type = 'put'
stock_ticker = 'MSFT'

# =============================================================================
#                               Working with data
# =============================================================================

# Downloading data
# Option data download
option = yf.download(option_ticker, start, end)


#Stock data download
stock_true = yf.download(stock_ticker, start, end)

# Data preparation
stock = pd.DataFrame(stock_true['Adj Close'].loc[option.index], option.index)
option.drop(option[['High', 'Open', 'Low', 'Close', 'Volume']],
            axis=1,
            inplace=True)

option['pct'] = option['Adj Close'].pct_change()
option.dropna(inplace=True)

stock['pct'] = stock['Adj Close'].pct_change()
stock.dropna(inplace=True)

# Data visualozation
stock_true['Adj Close'].plot(color='black')
plt.title('Stock price')
plt.show()

option['Adj Close'].plot(color='red')
plt.title('Option price')
plt.show()

stock['pct'].plot(color='black')
option['pct'].plot(color='red')
plt.title('Stock vs Option % change')
plt.show()

# =============================================================================
#                                   Delta hedging
# =============================================================================

# Separate dataframe for hedging proceedures
hedging = pd.DataFrame()
hedging['Stock'] = stock['Adj Close']
hedging['Put option'] = option['Adj Close']
hedging['Stock delta'] = hedging['Stock'].diff()
hedging['Option delta'] = hedging['Put option'].diff()
hedging.dropna(inplace=True)

hedging['Rate of change'] = [o/s for o, s in zip(hedging['Option delta'],
                                                 hedging['Stock delta'])]

hedging['Option position'] = 1 * 1
hedging['Stock position'] = 1 * 1 *hedging['Rate of change']

# Rebalancing portfolio of 1 stock and 1 option if needed
for index in range(1, len(hedging)):
    if (hedging['Rate of change'].iloc[index] !=
        hedging['Rate of change'].iloc[index-1]):   #check for neccessity
        print('Rebalancing portfoilo...\n Amount of stock: {}\n'
              'Amount of options: {}'.format(hedging['Stock position'].
                                             iloc[index],
                                             hedging['Option position'].
                                             iloc[index]))
        if (hedging['Rate of change'].iloc[index] >
            hedging['Rate of change'].iloc[index-1]):   #rebalancing action
            print('Amount of stock bought to balance portfoilio: {}'.format(
                (hedging['Rate of change'].iloc[index] -
                 hedging['Rate of change'].iloc[index-1])))
        else:
            print('Amount of stock sold to balance portfoilio: {}'.format(
                (hedging['Rate of change'].iloc[index] -
                 hedging['Rate of change'].iloc[index-1])))
        print('Your portfolio is now risk free')
        print('-------------------------------')
        


# Druzhkin Georgiy, 2020
# george.druzhkin@gmail.com