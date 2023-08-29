import MetaTrader5 as mt5
import rsi

if not mt5.initialize():
    print ("initialize() failed, error code = ", mt5.last_error())
    quit()

stocks_list = pd.read_csv('stocks.txt', header=None)
stocks_list = stocks_list.values.flatten().tolist()
    
TIMEFRAME = mt5.TIMEFRAME_H1
DATE_FROM = 0
NUM_CANDLES_LOOKBACK = 50
RSI_PERIOD = 14

rsi_df = pd.DataFrame(columns=['STOCK', f'RSI {RSI_PERIOD}'])

for stock in stocks_list:
    try:
        current_rsi = rsi.get_rsi_for_stock(mt5, stock, TIMEFRAME, DATE_FROM, NUM_CANDLES_LOOKBACK, RSI_PERIOD)
        rsi_df.loc[len(rsi_df)] = [stock, current_rsi]     
    except:
        continue



mt5.shutdown()
