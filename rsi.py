import pandas as pd
import numpy as np

def calculate_rsi(prices_df, rsi_period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame of stock prices.

    Parameters:
    - prices_df (pd.DataFrame): A DataFrame containing historical stock prices.
    - rsi_period (int, optional): The period for RSI calculation (default is 14).

    Returns:
    - rsi (float): The calculated RSI value for the given data.
    """
    
    price_changes = prices_df.diff().dropna()
    positive_changes = price_changes * 0
    negative_changes = positive_changes.copy()
    
    positive_changes[price_changes > 0] = price_changes[price_changes > 0]
    positive_changes[positive_changes.index[rsi_period-1]] = np.mean(positive_changes[:rsi_period])
    avg_positive_gains = positive_changes.drop(positive_changes.index[:(rsi_period-1)])   
    
    negative_changes[price_changes < 0] = -price_changes[price_changes < 0]
    negative_changes[negative_changes.index[rsi_period-1]] = np.mean(negative_changes[:rsi_period])
    avg_negative_losses = negative_changes.drop(negative_changes.index[:(rsi_period-1)])

    rs = pd.DataFrame.ewm(avg_positive_gains, com=rsi_period-1, adjust=False).mean() / \
         pd.DataFrame.ewm(avg_negative_losses, com=rsi_period-1, adjust=False).mean()
    
    rsi = round(((100 - 100 / (1 + rs)).iloc[-1]), 2)
    return rsi

def get_rsi_for_stock(mt5_conn, stock, timeframe, num_candles_sampling, rsi_period):
    """
    Returns the Relative Strength Index (RSI) for a specific stock

    Parameters:
    - mt5_conn (MetaTrader5 connection): A connection to MetaTrader 5 for data retrieval.
    - stock (str): The stock symbol or identifier.
    - timeframe (int): The timeframe for data retrieval (e.g., M1, M5, H1).
    - num_candles_sampling (int): The number of historical candles to sample for RSI calculation.
    - rsi_period (int): The period for RSI calculation.

    Returns:
    - rsi (float): The calculated RSI value for the specified stock and parameters.
    """
    
    rates = mt5_conn.copy_rates_from_pos(stock.strip(), timeframe, 0, num_candles_sampling)
    rates_df = pd.DataFrame(rates)
    rsi = calculate_rsi(rates_df['close'], rsi_period)
    return rsi




