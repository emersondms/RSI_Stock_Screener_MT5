import pandas as pd
import numpy as np
import MetaTrader5 as mt5

def get_rsi(df, period=14): #TODO rename function
    price_changes = df.diff().dropna()
    positive_changes = price_changes * 0
    negative_changes = positive_changes.copy()
    
    positive_changes[price_changes > 0] = price_changes[price_changes > 0]
    positive_changes[positive_changes.index[period-1]] = np.mean(positive_changes[:period])
    avg_positive_gains = positive_changes.drop(positive_changes.index[:(period-1)])   
    
    negative_changes[price_changes < 0] = -price_changes[price_changes < 0]
    negative_changes[negative_changes.index[period-1]] = np.mean(negative_changes[:period])
    avg_negative_losses = negative_changes.drop(negative_changes.index[:(period-1)])

    rs = pd.DataFrame.ewm(avg_positive_gains, com=period-1, adjust=False).mean() / \
         pd.DataFrame.ewm(avg_negative_losses, com=period-1, adjust=False).mean()
    
    rsi = round(((100 - 100 / (1 + rs)).iloc[-1]), 2)
    return rsi
    
def get_rsi_df(mt5_conn, stocks_list, rsi_period, timeframe, date_from, num_candles_lookback): #TODO rename function
    rsi_df = pd.DataFrame(columns=['STOCK', f'RSI {rsi_period}'])

    for stock in stocks_list:
        try:
            rates = mt5_conn.copy_rates_from_pos(stock.strip(), timeframe, date_from, num_candles_lookback)
            rates_df = pd.DataFrame(rates)
            current_rsi = rsi(rates_df['close'], rsi_period)
            rsi_df.loc[len(rsi_df)] = [stock, current_rsi]     
        except:
            continue
    
    return rsi_df


