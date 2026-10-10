# finance_functions

A collection of Python scripts I created to analyse financial data. Market data is downloaded from Yahoo Finance via [`yfinance`](https://github.com/ranaroussi/yfinance).

## Scripts

| File | What it does |
|------|--------------|
| `RSI_function.py` | Calculates and plots the Relative Strength Index (RSI) for a list of tickers. Includes a commented-out example that runs the S&P 500 constituents through the function. |
| `MACD_function.py` | Calculates and plots the MACD line and its signal line for a list of tickers. |
| `portfolio.py` | Builds a portfolio of stocks, simulates random portfolios and estimates their return and volatility. |
| `trendlines.py` | Finds demand and supply pivot points and draws trendlines for a ticker. |
| `demand_trendlines.py` | Finds demand pivot points and draws demand trendlines for a ticker. |
| `delta_hedging.py` | Delta hedging example for a stock option (e.g. an MSFT put). |
| `hf_dataloader.py` | Polls the latest price of a ticker (e.g. `BTC-USD`) once a minute to collect a high-frequency price series. |

## Requirements

- Python 3
- `yfinance`, `pandas`, `numpy`, `matplotlib`, `mplfinance`
- `requests`, `beautifulsoup4`, `lxml` (only for the optional S&P 500 example in `RSI_function.py`)

```bash
pip install yfinance pandas numpy matplotlib mplfinance
```

## Usage

Each script is self-contained. Edit the inputs at the top of the file (tickers, start and end dates) and run it:

```bash
python RSI_function.py
```
