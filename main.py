import MetaTrader5 as mt5
import pandas as pd
import tkinter as tk
from jproperties import Properties
import rsi
import gui

# Initialize MT5 connection
if not mt5.initialize():
    print ("initialize() failed, error code = ", mt5.last_error())
    quit()

# Load the stocks list from txt file
stocks_list = pd.read_csv('stocks.txt', header=None)
stocks_list = stocks_list.values.flatten().tolist()
    
# load properties from file
props = Properties()
with open('screener.properties', 'rb') as config_file:
    props.load(config_file)

RAW_TIMEFRAME = props.get("TIMEFRAME").data
TIMEFRAME = getattr(mt5, RAW_TIMEFRAME, None)
NUM_CANDLES_SAMPLING = int(props.get("NUM_CANDLES_SAMPLING").data)
RSI_PERIOD = int(props.get("RSI_PERIOD").data)
RSI_OVERSOLD_LEVEL = int(props.get("RSI_OVERSOLD_LEVEL").data)

# Returns a dataframe with STOCK|RSI information
def get_filled_rsi_df():
    rsi_df = pd.DataFrame(columns=['STOCK', f'RSI_{RSI_PERIOD} {RAW_TIMEFRAME}'])

    # Fill the dataframe with stocks below RSI_OVERSOLD_LEVEL
    for stock in stocks_list:
        try:
            current_rsi = rsi.get_rsi_for_stock(mt5, stock, TIMEFRAME, NUM_CANDLES_SAMPLING, RSI_PERIOD)
            if (float(current_rsi) <= RSI_OVERSOLD_LEVEL):
                rsi_df.loc[len(rsi_df)] = [stock, current_rsi]     
        except:
            continue

    return rsi_df        

# Create the main window and configure the button command to pass the updated data
root = tk.Tk()
window = gui.Window(root, get_filled_rsi_df())
window.refresh_button.config(command=lambda: window.insert_data(get_filled_rsi_df()))
root.mainloop()
mt5.shutdown()
