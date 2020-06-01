import yfinance as yf
import datetime as dt
import pandas as pd
import time

now = dt.datetime.now()
start = dt.datetime(2020,6,1)
end = dt.datetime.now()
finish = dt.datetime(year=2020,
                     month=5,
                     day=31,
                     hour=20)
hft = pd.DataFrame()

def p_download(ticker):
    aapl = yf.download(ticker, start, end)['Adj Close']
    aapl = pd.DataFrame(aapl)
    last_price = float(aapl.iloc[-1])
    
    return last_price


prices = []
index = []
count = 0
time_step = dt.timedelta(minutes=1)
while count < 1000:
    price = p_download('BTC-USD')
    prices = prices + [price]
    index = index + [dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    count += 1
    time.sleep(60)
    
prices = pd.DataFrame({'Adj Close':prices}, index)