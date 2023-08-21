import pandas as pd
import numpy as np

def get(df, period=14):
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




