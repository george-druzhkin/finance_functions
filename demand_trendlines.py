def demand_pivot_points(ticker, start, end):
    # Downloading data
    import yfinance as yf
    import pandas as pd
    import numpy as np
    
    df = yf.download(ticker, start, end)
    df.reset_index(inplace=True)
    
    # Data manipulation
    # Defining demand points
    demand_ppp = {}
    high = df['High']
    close = df['Adj Close']
    date = df['Date']
    
    for index in range(len(df)):
        if index == len(df)-1:
            break
        else:
            if (high.iloc[index] > high.iloc[index+1] and
                high.iloc[index] > high.iloc[index-1] and
                high.iloc[index] > close.iloc[index-2]):
                demand_ppp[df.index[index]] = [date.iloc[index],
                                               high.iloc[index]]
            else:
                demand_ppp[df.index[index]] = [date.iloc[index],
                                               np.nan]
    demand_ppp[df.index[-1]] = [date.iloc[-1], np.nan]
    
    # Creating dataframes with demand points (with NaN and without)
    demand_ppp = pd.DataFrame(demand_ppp.values(),
                              index=demand_ppp.keys(),
                              columns=['Date','Price'])
    demand_ppp_na = demand_ppp.dropna().copy()
    
    # Disrading two consecutive points
    demand_ppp_na_copy = demand_ppp_na.copy()
    price = demand_ppp_na_copy['Price']
    
    for index in range(len(demand_ppp_na_copy)):
        if index == len(demand_ppp_na_copy) - 1:
            break
        if (price.iloc[index] > price.iloc[index-1] and
            price.iloc[index] < price.iloc[index+1]):
            demand_ppp_na.drop(demand_ppp_na_copy.index[index], inplace=True)
            demand_ppp['Price'].loc[demand_ppp_na_copy.index[index]] = np.nan
    
    # Discarding points that break through the slope
    demand_slope = {}
    price = demand_ppp_na['Price']
    
    for index in range(1,len(demand_ppp_na)):
        delta_x = demand_ppp_na.index[index]-demand_ppp_na.index[index-1]
        delta_y = price.iloc[index] - price.iloc[index-1]           
        demand_slope[demand_ppp_na.index[0]] = 0
        demand_slope[demand_ppp_na.index[index]] = delta_y / delta_x
    
    demand_slope = pd.DataFrame(demand_slope.values(),
                            demand_slope.keys(),
                            columns=['Slope'])
    
    high = df['High']
    close = df['Adj Close']
    slope = demand_slope['Slope']
    
    for index, row in demand_slope.iterrows():
        if (close.loc[index+1] > (high.loc[index] + slope.loc[index]*1)):
            demand_ppp['Price'].iloc[index] = np.nan
            demand_ppp_na.drop([index], inplace=True)
            demand_slope.drop([index], inplace=True)
    
    # Discard when there are two consecutive positive slopes
    slope = demand_slope['Slope']
    
    for index in range(len(demand_slope)):
        if index == len(demand_slope) - 1:
            break
        else:
            if slope.iloc[index] > 0 and slope.iloc[index+1] > 0:
                demand_ppp_na.drop([demand_slope.index[index]], inplace=True)
                demand_ppp.iloc[demand_slope.index[index]] = np.nan
    
    # Plotting
    import mplfinance as mpf

    # Plot of demand pivot points 
    highs = mpf.make_addplot(demand_ppp['Price'],
                             type='scatter',
                             markersize=100,
                             color='red',
                             marker='v')
    
    # Trendlines plot
    demand_trendlines = []
    price = demand_ppp_na['Price']
    d = demand_ppp_na['Date']
    
    for index in range(len(demand_ppp_na)):
        if index == len(demand_ppp_na)-1:
            break
        else:
            if (price.iloc[index] > price.iloc[index+1]):
                demand_trendlines.append([(d.iloc[index].strftime('%Y-%m-%d'),
                                           int(price.iloc[index])),
                                          (d.iloc[index+1].strftime('%Y-%m-%d'),
                                           int(price.iloc[index+1]))])
    
    # Last trendline enlargement
    price = demand_ppp_na['Price']
    slope = demand_slope['Slope']

    if price.iloc[-1] < price.iloc[-2]:
        timedelta = int(df.index[-1]-demand_ppp_na.index[-1])
        x1 = (demand_ppp_na['Date'].iloc[-1].strftime('%Y-%m-%d'),
              int(demand_ppp_na['Price'].iloc[-1]))
        x2 = (df['Date'].iloc[-1].strftime('%Y-%m-%d'),
              int(price.iloc[-1] + (timedelta * slope.iloc[-1])))
        demand_trendlines.append([x1, x2])
        
    # Trendline breakthroughs
    price = demand_ppp_na['Price']
    date = demand_ppp_na['Date']
    slope = demand_slope['Slope']
    
    for index in range(1, len(demand_ppp_na)):
        if index == len(demand_ppp_na)-1:
            break
        else:
            if price.iloc[index] < price.iloc[index+1]:
                x1 = (date.iloc[index].strftime('%Y-%m-%d'),
                      price.iloc[index])
                timedelta = (demand_ppp_na.index[index+1] -
                             demand_ppp_na.index[index])
                x2 = (date.iloc[index+1].strftime('%Y-%m-%d'),
                      price.iloc[index] + timedelta *
                      slope.loc[demand_ppp_na.index[index]])
                demand_trendlines.append([x1, x2])
    
    # Final mpf plot
    mpf.mplfinance.plot(df.set_index(df['Date']), 
                        type='candle',
                        volume=False , 
                        style='classic',
                        addplot=highs,
                        title='Demand price pivot points {}'.format(ticker),
                        alines=demand_trendlines)

    return (df, demand_ppp_na)

# =============================================================================
#                           data processing
# =============================================================================
import datetime as dt
start = dt.date(2019,6,1)
end = dt.date(2019,12,3)


gmkn = demand_pivot_points('GMKN.ME', start, end)
yandex = demand_pivot_points('YNDX.ME',start,end)