import pandas as pd
import numpy as np

df = pd.read_csv(r"E:\Tung\Python\VcreamProject\cache\ALL.csv")

df.drop(['Unnamed: 0'], axis = 1, inplace=True)

def moving_average(panel_data):

    panel_data["ma_10"] = panel_data.groupby('Ticker')['Close'].rolling(10, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_20"] = panel_data.groupby('Ticker')['Close'].rolling(20, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_50"] = panel_data.groupby('Ticker')['Close'].rolling(50, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_100"] = panel_data.groupby('Ticker')['Close'].rolling(100, min_periods=1).mean().reset_index(drop=True).to_list()
    
    return panel_data