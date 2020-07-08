# =============================================================================
#                           Demand price pivot points
# =============================================================================
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
    close = df['Close']
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
    close = df['Close']
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
                                           (price.iloc[index])),
                                          (d.iloc[index+1].strftime('%Y-%m-%d'),
                                           (price.iloc[index+1]))])
    
    # Last trendline enlargement
    price = demand_ppp_na['Price']
    slope = demand_slope['Slope']

    if price.iloc[-1] < price.iloc[-2]:
        timedelta = int(df.index[-1]-demand_ppp_na.index[-1])
        x1 = (demand_ppp_na['Date'].iloc[-1].strftime('%Y-%m-%d'),
              (demand_ppp_na['Price'].iloc[-1]))
        x2 = (df['Date'].iloc[-1].strftime('%Y-%m-%d'),
              (price.iloc[-1] + (timedelta * slope.iloc[-1])))
        demand_trendlines.append([x1, x2])
        
    '''# Trendline breakthroughs
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
                demand_trendlines.append([x1, x2])'''
    
    # Final mpf plot
    mpf.mplfinance.plot(df.set_index(df['Date']), 
                        type='candle',
                        volume=False , 
                        style='classic',
                        addplot=highs,
                        title='Demand price pivot points {}'.format(ticker),
                        alines=demand_trendlines)

    return (df, demand_ppp, demand_trendlines)



# =============================================================================
#                           Supply price pivot points
# =============================================================================
def supply_pivot_points(ticker, start, end):
    # Downloading data
    import yfinance as yf
    import pandas as pd
    import numpy as np
    
    df = yf.download(ticker, start, end)
    df.reset_index(inplace=True)
    
    # Data manipulation
    # Defining supply points
    supply_ppp = {}
    low = df['Low']
    close = df['Close']
    date = df['Date']
    
    for index in range(len(df)):
        if index == len(df)-1:
            break
        else:
            if (low.iloc[index] < low.iloc[index+1] and
                low.iloc[index] < low.iloc[index-1] and
                low.iloc[index] < close.iloc[index-2]):
                supply_ppp[df.index[index]] = [date.iloc[index],
                                               low.iloc[index]]
            else:
                supply_ppp[df.index[index]] = [date.iloc[index],
                                               np.nan]
    supply_ppp[df.index[-1]] = [date.iloc[-1], np.nan]

    # Creating dataframes with supply points (with NaN and without)
    supply_ppp = pd.DataFrame(supply_ppp.values(),
                              index=supply_ppp.keys(),
                              columns=['Date','Price'])
    supply_ppp_na = supply_ppp.dropna().copy()
    
    # Disrading two consecutive increasing points
    supply_ppp_na_copy = supply_ppp_na.copy()
    price = supply_ppp_na_copy['Price']
    
    for index in range(len(supply_ppp_na_copy)):
        if index == len(supply_ppp_na_copy) - 1:
            break
        if (price.iloc[index] < price.iloc[index-1] and
            price.iloc[index] > price.iloc[index+1]):
            supply_ppp_na.drop(supply_ppp_na_copy.index[index], inplace=True)
            supply_ppp['Price'].loc[supply_ppp_na_copy.index[index]] = np.nan
    
    # Discarding points that break through the slope
    supply_slope = {}
    price = supply_ppp_na['Price']
    
    for index in range(1,len(supply_ppp_na)):
        delta_x = supply_ppp_na.index[index]-supply_ppp_na.index[index-1]
        delta_y = price.iloc[index] - price.iloc[index-1]           
        supply_slope[supply_ppp_na.index[0]] = 0
        supply_slope[supply_ppp_na.index[index]] = delta_y / delta_x
    
    supply_slope = pd.DataFrame(supply_slope.values(),
                            supply_slope.keys(),
                            columns=['Slope'])
    
    low = df['Low']
    close = df['Close']
    slope = supply_slope['Slope']
    
    for index, row in supply_slope.iterrows():
        if (close.loc[index+1] < (low.loc[index] + slope.loc[index]*1)):
            supply_ppp['Price'].iloc[index] = np.nan
            supply_ppp_na.drop([index], inplace=True)
            supply_slope.drop([index], inplace=True)
    
    # Discard when there are two consecutive negative slopes
    slope = supply_slope['Slope']
    
    for index in range(len(supply_slope)):
        if index == len(supply_slope) - 1:
            break
        else:
            if slope.iloc[index] < 0 and slope.iloc[index+1] < 0:
                supply_ppp_na.drop([supply_slope.index[index]], inplace=True)
                supply_ppp.iloc[supply_slope.index[index]] = np.nan
    
    # Plotting
    import mplfinance as mpf

    # Plot of supply pivot points 
    lows = mpf.make_addplot(supply_ppp['Price'],
                             type='scatter',
                             markersize=100,
                             color='green',
                             marker='^')
    
    # Trendlines plot
    supply_trendlines = []
    price = supply_ppp_na['Price']
    d = supply_ppp_na['Date']
    
    for index in range(len(supply_ppp_na)):
        if index == len(supply_ppp_na)-1:
            break
        else:
            if (price.iloc[index] < price.iloc[index+1]):
                supply_trendlines.append([(d.iloc[index].strftime('%Y-%m-%d'),
                                           (price.iloc[index])),
                                          (d.iloc[index+1].strftime('%Y-%m-%d'),
                                           (price.iloc[index+1]))])
    
    # Last trendline enlargement
    price = supply_ppp_na['Price']
    slope = supply_slope['Slope']

    if price.iloc[-1] > price.iloc[-2]:
        timedelta = int(df.index[-1]-supply_ppp_na.index[-1])
        x1 = (supply_ppp_na['Date'].iloc[-1].strftime('%Y-%m-%d'),
              supply_ppp_na['Price'].iloc[-1])
        x2 = (df['Date'].iloc[-1].strftime('%Y-%m-%d'),
              price.iloc[-1] + (timedelta * slope.iloc[-1]))
        supply_trendlines.append([x1, x2])
        
    '''# Trendline breakthroughs
    price = supply_ppp_na['Price']
    date = supply_ppp_na['Date']
    slope = supply_slope['Slope']
    
    for index in range(1, len(supply_ppp_na)):
        if index == len(supply_ppp_na)-1:
            break
        else:
            if price.iloc[index] > price.iloc[index+1]:
                x1 = (date.iloc[index].strftime('%Y-%m-%d'),
                      price.iloc[index])
                timedelta = (supply_ppp_na.index[index+1] -
                             supply_ppp_na.index[index])
                x2 = (date.iloc[index+1].strftime('%Y-%m-%d'),
                      price.iloc[index] + timedelta *
                      slope.loc[supply_ppp_na.index[index]])
                supply_trendlines.append([x1, x2])'''
    
    # Final mpf plot
    mpf.mplfinance.plot(df.set_index(df['Date']), 
                        type='candle',
                        volume=False , 
                        style='classic',
                        addplot=lows,
                        title='Supply price pivot points {}'.format(ticker),
                        alines=supply_trendlines)

    return (df, supply_ppp, supply_trendlines)



# =============================================================================
#                       Supply and demand points united
# =============================================================================
def trendlines(ticker, start, end):
    demand = demand_pivot_points(ticker, start, end)
    supply = supply_pivot_points(ticker, start, end)
    
    # List of trendlines
    trendlines = []
    demand_trendlines = demand[2]
    supply_trendlines = supply[2]
    for i in demand_trendlines:
        trendlines.append(i)
    for i in supply_trendlines:
        trendlines.append(i)
    
    # Dataframes with points
    demand_ppp = demand[1]
    supply_ppp = supply[1]
    df = supply[0]
    
    # Plotting
    import mplfinance as mpf
    points = [mpf.make_addplot(demand_ppp['Price'],
                               type='scatter',
                               markersize=100,
                               color='red',
                               marker='v'),
              mpf.make_addplot(supply_ppp['Price'],
                               type='scatter',
                               markersize=100,
                               color='green',
                               marker='^')]
    
    mpf.mplfinance.plot(df.set_index(df['Date']), 
                        type='ohlc',
                        volume=False , 
                        style='classic',
                        addplot=points,
                        title='Trendlines {}'.format(ticker),
                        alines=trendlines)

    return(demand, supply)

# =============================================================================
#                                   Results
# =============================================================================

import datetime as dt
start = dt.date(2020,3,1)
end = dt.date.today()

eurusd = trendlines('GBPRUB=X', start, end)
