import pandas as pd
import numpy as np
import MetaTrader5 as mt5

def calculate_rsi(prices_df, rsi_period=14):
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

def get_rsi_for_stock(mt5_conn, stock, timeframe, date_from, num_candles_lookback, rsi_period):
    rates = mt5_conn.copy_rates_from_pos(stock.strip(), timeframe, date_from, num_candles_lookback)
    rates_df = pd.DataFrame(rates)
    rsi = calculate_rsi(rates_df['close'], rsi_period)
    return rsi




