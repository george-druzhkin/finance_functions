import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


# =============================================================================
#                               Input data
# =============================================================================
#Initial inputs - input set(!!!) of tickers in the corresponding list
#Change data in start/end variable as you wish

tickers = ['AAPL']  #you can add any number of them here
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

# Download data in accrdance to ticker, start and end date
stocks = pd.DataFrame(yf.download(tickers, start, end)['Adj Close'])
stocks.columns = tickers

# =============================================================================
#                               RSI function
# =============================================================================
# RSI = 100 - (100/(1-RS)), where RS = avg_up_move / avg_down_move
def rsi(data, period):
    # Creating dataframe for storing all the inforamtion
    rsi_df = pd.DataFrame()
    
    for ticker in tickers:
        # Getting the upside and downside movement columns
        rsi_df['move'] = data[ticker].diff()
        rsi_df['up_move'] = [delta if delta>0 else 0
                             for delta in rsi_df['move']]
        rsi_df['down_move'] = [delta if delta<0 else 0
                               for delta in rsi_df['move']]
        
        # Calculating average movement with SMA method
        rsi_df['avg_up'] = rsi_df['up_move'].rolling(period).mean()
        rsi_df['avg_down'] = rsi_df['down_move'].rolling(period).mean()
        
        # Calculating relative strength
        rsi_df['rs'] = rsi_df['avg_up'] / rsi_df['avg_down']
        
        # Calculating Relative Strength Index (RSI)
        rsi_df[ticker] = 100 - (100/(1-rsi_df['rs']))
        
        # Graphical visualisation
        rsi_df[ticker].plot(kind='line', color='black')
        plt.title('{} RSI'.format(ticker)+'{}'.format(period))
        plt.show()
        
    return rsi_df[tickers]

rsi_table = rsi(stocks, 14)
# Now you can simply call 'Name of your DataFrame for rsi' = rsi(data, period)
# and you will get one DataFrame with RSI values for different 

# A fun example: running 500 stocks from s&p500 through the function
# Just paste the following before creating the list of tickers (on line 12)
'''
import requests
import bs4 as bs

# Stock list creation
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('. ', '-')
        ticker = ticker[:-1]
        tickers.append(ticker)

    return tickers
tickers = save_sp500_tickers()
tickers.remove('BRK.B')
tickers.remove('BF.B')
tickers.remove('DOW')
'''

# Enjoy it!


# contact: george.druzhkin@gmail.com
