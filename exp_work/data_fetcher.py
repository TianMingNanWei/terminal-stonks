import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetches stock data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        period (str): The period for which to fetch data (e.g., "1y", "2y").
        interval (str): The data interval ("1d", "1wk", "1mo").

    Returns:
        pd.DataFrame: A DataFrame with OHLCV data, or an empty DataFrame if the ticker is invalid.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    if data.empty:
        print(f"Error: Could not find data for ticker '{ticker}'. Please check the symbol.")
        return pd.DataFrame()
    
    # Make sure the essential columns are present
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in data.columns for col in required_columns):
        print(f"Error: Fetched data for {ticker} is missing required columns.")
        return pd.DataFrame()

    return data 