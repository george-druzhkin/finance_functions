# =============================================================================
#                       Creating portfolio of stocks
# =============================================================================
tickers = ['LKOH.ME', 'YNDX.ME', 'PLZL.ME', 'ALRS.ME']
tickers.sort()


# =============================================================================
#                       Additional functions block
# =============================================================================
# Function to create portfolio
def create_portfolio(ticker):
    # Input information
    import yfinance as yf
    import datetime as dt
    start = dt.datetime(2018,1,1)
    end = dt.datetime.now()
    prices = yf.download(tickers, start, end)['Adj Close']
    returns = prices.pct_change().dropna()
    
    return(returns)

# Calculation of portfolio return and volatility
def return_and_volatility(returns, weights, cov_matrix):
    import numpy as np
    mean_return = np.dot(((1+np.mean(returns))**252) - 1, weights)
    mean_std = np.sqrt((np.dot(weights.T, np.dot(cov_matrix, weights)))*252)
    return (mean_return, mean_std)

# Random portfolios (for GMS and MSR portfolios)
def random_portfolios(num_portfolios,
                      returns,
                      risk_free_rate):
    import pandas as pd
    import numpy as np
    results = pd.DataFrame(columns=['Std','Return','Sharpe'])
    weight_pd = pd.DataFrame(columns=tickers)
    cov_matrix = returns.cov()
    for i in range(num_portfolios):
        weights = np.random.random(4)
        weights /= np.sum(weights)
        weight_pd.loc[i,tickers] = (weights)
        
        portfolio_return, portfolio_std = return_and_volatility(returns,
                                                                weights,
                                                                cov_matrix)
        
        results.loc[i,'Return'] = portfolio_return
        results.loc[i,'Std'] = portfolio_std
        
        # Sharpe ratio
        results.loc[i,'Sharpe'] = ((portfolio_return - risk_free_rate) /
                                   portfolio_std)

    return(results, weight_pd)

# Function to get main parameters of portfolio
def stock_parameters(returns):
    import pandas as pd
    stock_params = pd.DataFrame()
    # Correlation and covariance matrices
    # Correlation maxrix
    corr_matrix = returns[tickers].corr()
    
    # Annualized covariance matrix
    cov_matrix = returns[tickers].cov() * 252
        
    # Dataframe with annualized portfolio parameters (the 4 moments)
    import numpy as np
    # Mean (annualizaed)
    for ticker in tickers:
        stock_params.loc['Mean',ticker] = ((1+np.mean(returns[ticker]))
                                              **252) - 1
    
    # Variance (annualized)
    for ticker in tickers:
        stock_params.loc['Variance',ticker] = np.var(returns[ticker]) * 252

    # Standard deviation (annualized)
    for ticker in tickers:
        stock_params.loc['Std',ticker] = (np.std(returns[ticker])*
                                         np.sqrt(252))
    # Skewness
    from scipy.stats import skew
    for ticker in tickers:
        stock_params.loc['Skewness',ticker] = skew(returns[ticker])
            
    # Kurtosis
    from scipy.stats import kurtosis
    for ticker in tickers:
        stock_params.loc['ExKurtosis',ticker] = kurtosis(returns[ticker])
        
    # Shapiro ratio for normality
    from scipy.stats import shapiro
    for ticker in tickers:
        if shapiro(returns[ticker])[1] <= 0.05:
            stock_params.loc['Shapiro Ratio'] = 'Non-normal'
        else:
            stock_params.loc['Shapiro Ratio'] = 'Normal'
    return (stock_params, corr_matrix, cov_matrix)

def portfolio_parameters(returns, stock_params, cov_matrix):
    # Dataframe with annualized portfolio parameters (the 4 moments)
    import numpy as np
    import pandas as pd
    port_params = pd.DataFrame()

    # Mean (annualizaed)
    port_params.loc['Mean','Portfolio'] = np.dot(stock_params.loc['Mean',
                                                                  tickers],
                                                 stock_params.loc['Weight',
                                                                  tickers])
    
    # Variance (annualized)

    port_params.loc['Variance','Portfolio'] = np.dot(stock_params.
                                                     loc['Weight',tickers].T,
                        np.dot(cov_matrix,stock_params.loc['Weight',tickers]))

    # Standard deviation (annualized)
    port_params.loc['Std','Portfolio'] = np.sqrt(port_params.loc['Variance',
                                                                 'Portfolio'])
    '''# Skewness
    from scipy.stats import skew
    port_params.loc['Skewness','Portfolio'] = skew(returns['Portfolio'])
            
    # Kurtosis
    from scipy.stats import kurtosis
    port_params.loc['ExKurtosis','Portfolio'] = kurtosis(returns['Portfolio'])
        
    # Shapiro ratio for normality
    from scipy.stats import shapiro
    if shapiro(returns['Portfolio'])[1] <= 0.05:
        port_params.loc['Shapiro Ratio','Portfolio'] = 'Non-normal'
    else:
        port_params.loc['Shapiro Ratio','Portfolio'] = 'Normal' '''
    return (port_params)

def weighted_returns(returns, weights):
    returns['Portfolio'] = returns.mul(weights,axis=1).sum(axis=1)

# Graphical ilustration of portfolio performance
def portfolio_plot(returns, kind):
    import matplotlib.pyplot as plt
    for name, value in returns.iteritems():
        plt.plot((1+returns[name]).cumprod()-1, label=name)
    plt.legend()
    plt.title(kind+' Portfolio')
    plt.show()


# =============================================================================
#                               Main function
# =============================================================================
def portfolio(ticker, kind):
    returns = create_portfolio(ticker)
    stock_params, corr_matrix, cov_matrix = stock_parameters(returns)
    if kind == 'MarketCap Weighted':
        # Capitalization of companies
        stock_params.loc['MarketCap', tickers[0]] = 464830529536
        stock_params.loc['MarketCap', tickers[1]] = 3454297702400
        stock_params.loc['MarketCap', tickers[2]] = 1594318913536
        stock_params.loc['MarketCap', tickers[3]] = 1139196690432
        
        # Weights of portfolio
        stock_params.loc['Weight',tickers] = (stock_params.loc['MarketCap',
                                                             tickers]/
                                             sum(stock_params.loc['MarketCap',
                                                                 tickers]))
        weighted_returns(returns, stock_params.loc['Weight'])
        
        # Plot of the performance
        portfolio_plot(returns, kind)

    if kind == 'GMV':
        # Creating random portfoilios
        random = random_portfolios(1000, returns, 0.05)
        results = random[0]
        weight_pd = random[1]
        optimal_weight = weight_pd.loc[results['Std'] ==
                               results['Std'].min()].values
        
        # Weights of portfolio
        stock_params.loc['Weight',tickers] = optimal_weight
        weighted_returns(returns, stock_params.loc['Weight'])
        
        # Portfolio parameters
        port_params = portfolio_parameters(returns, stock_params,cov_matrix)
        
        # Plot of random combinations
        import matplotlib.pyplot as plt
        plt.scatter(random[0]['Std'], 
                    random[0]['Return'], 
                    alpha=0.3)
        plt.scatter(port_params.loc['Std'], 
                    port_params.loc['Mean'], 
                    color='red', alpha=1, s=50)
        plt.axhline(port_params.loc['Mean', 'Portfolio'],
                    color='orange', ls='--')
        plt.title('Global Minimum Volatility combination')
        plt.show()
        
        # Plot of the performance
        portfolio_plot(returns, kind)
        
    if kind == 'MSR':
        # Creating random portfolio
        random = random_portfolios(1000, returns, 0.05)
        results = random[0]
        weight_pd = random[1]
        optimal_weight = weight_pd.loc[results['Sharpe'] ==
                               results['Sharpe'].max()].values
        
        # Weights of portfolio
        stock_params.loc['Weight',tickers] = optimal_weight
        weighted_returns(returns, stock_params.loc['Weight'])
        
        # Portfolio parameters for scatter plot
        port_params = portfolio_parameters(returns, stock_params,cov_matrix)
        
        # Plot of random combinations
        import matplotlib.pyplot as plt
        plt.scatter(random[0]['Std'], 
                    random[0]['Return'], 
                    alpha=0.3)
        plt.scatter(port_params.loc['Std'], 
                    port_params.loc['Mean'], 
                    color='red', alpha=1, s=50)
        '''plt.axhline(port_params.loc['Mean', 'Portfolio'],
                    color='orange', ls='--')'''
        plt.title('Maximum Sharpe Ratio combination')
        plt.show()
        
        # Plot of the performance
        portfolio_plot(returns, kind)
    
    port_params = portfolio_parameters(returns, stock_params,cov_matrix)
    import pandas as pd
    params = pd.concat((stock_params,port_params),axis=1)
    
    return(params,
           returns['Portfolio'],
           corr_matrix)
 

# =============================================================================
#                               Results block
# =============================================================================
port1 = portfolio(tickers, 'MarketCap Weighted')   
port2 = portfolio(tickers, 'GMV') 
port3 = portfolio(tickers, 'MSR')