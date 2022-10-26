import pandas as pd
import numpy as np 

pd.set_option('mode.chained_assignment', None)

# Process Trend Group

# 1. Moving Average
def moving_average(panel_data):

    panel_data["ma_10"] = panel_data.groupby('Ticker')['Close'].rolling(10, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_20"] = panel_data.groupby('Ticker')['Close'].rolling(20, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_50"] = panel_data.groupby('Ticker')['Close'].rolling(50, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["ma_100"] = panel_data.groupby('Ticker')['Close'].rolling(100, min_periods=1).mean().reset_index(drop=True).to_list()
    
    return panel_data


# 2. Triple EMA
def triple_ema(panel_data):
    panel_data['ema_1'] = panel_data.groupby('Ticker')['Close'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()
    panel_data['ema_2'] = panel_data.groupby('Ticker')['ema_1'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()
    panel_data['ema_3'] = panel_data.groupby('Ticker')['ema_2'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()

    panel_data['triple_ema'] = 3*panel_data['ema_1'] - 3*panel_data['ema_2'] + panel_data['ema_3']
    
    del panel_data['ema_1']
    del panel_data['ema_2']
    del panel_data['ema_3']
    
    return panel_data


# 3. Rate of Change ROC
def roc(panel_data):
    panel_data['roc_5'] = panel_data.groupby('Ticker')['Close'].diff(5)/panel_data.groupby('Ticker')['Close'].shift(5)
    panel_data['roc_10'] = panel_data.groupby('Ticker')['Close'].diff(10)/panel_data.groupby('Ticker')['Close'].shift(10)
    panel_data['roc_20'] = panel_data.groupby('Ticker')['Close'].diff(20)/panel_data.groupby('Ticker')['Close'].shift(20)
    panel_data['roc_40'] = panel_data.groupby('Ticker')['Close'].diff(40)/panel_data.groupby('Ticker')['Close'].shift(40)
    panel_data['roc_80'] = panel_data.groupby('Ticker')['Close'].diff(80)/panel_data.groupby('Ticker')['Close'].shift(80)

    return panel_data
    

# 4. Normalized Average True Range
def natr(panel_data):
    panel_data['previous_close'] = panel_data.groupby('Ticker')['Close'].shift(1)
    panel_data['high-low'] = panel_data['High'] - panel_data['Low']
    panel_data['high-pc'] = np.abs(panel_data['High'] - panel_data['previous_close'])
    panel_data['low-pc'] = np.abs(panel_data['Low'] - panel_data['previous_close'])
    panel_data['true_range'] = np.max(panel_data[['high-low', 'high-pc', 'low-pc']], axis=1)

    panel_data['atr_10'] = panel_data.groupby('Ticker')['true_range'].rolling(10).mean().reset_index(drop=True).to_list()
    panel_data['atr_15'] = panel_data.groupby('Ticker')['true_range'].rolling(15).mean().reset_index(drop=True).to_list()
    panel_data['atr_20'] = panel_data.groupby('Ticker')['true_range'].rolling(20).mean().reset_index(drop=True).to_list()

    panel_data['natr_10'] = panel_data['atr_10']/panel_data['Close']*100
    panel_data['natr_15'] = panel_data['atr_15']/panel_data['Close']*100
    panel_data['natr_20'] = panel_data['atr_20']/panel_data['Close']*100
    
    del panel_data['previous_close']
    del panel_data['high-low']
    del panel_data['high-pc']
    del panel_data['low-pc']
    del panel_data['true_range']
    del panel_data['atr_10']
    del panel_data['atr_15']
    del panel_data['atr_20']

    return panel_data


# 5. Disparity Index
def disparity_index(panel_data, lookbacks: int):
    panel_data['moving_average_14'] = panel_data.groupby('Ticker')['Close'].rolling(lookbacks).mean().reset_index(drop=True).to_list()
    panel_data[f'disparity_index_{lookbacks}'] = (panel_data['Close'] - panel_data['moving_average_14'])/(panel_data['moving_average_14'])*100
    
    del panel_data['moving_average_14']
    
    return panel_data


# Process Momentum Group
# 1. RSI
def rsi(panel_data, lookback: int):
    panel_data['delta'] = panel_data.groupby('Ticker')['Close'].diff()
    panel_data['up'] = panel_data['delta'].clip(lower=0)
    panel_data['down'] = -1*panel_data['delta'].clip(upper=0)

    panel_data['ema_up'] = panel_data.groupby('Ticker')['up'].ewm(com=lookback, adjust=False).mean().reset_index(drop=True).to_list()
    panel_data['ema_down'] = panel_data.groupby('Ticker')['down'].ewm(com=lookback, adjust=False).mean().reset_index(drop=True).to_list()

    panel_data['rs'] = panel_data['ema_up']/panel_data['ema_down']
    panel_data[f'rsi_{lookback}'] = 100 - (100/(1+panel_data['rs']))
    
    del panel_data['delta']
    del panel_data['up']
    del panel_data['down']
    del panel_data['ema_up']
    del panel_data['ema_down']
    del panel_data['rs']
    
    return panel_data


# 2. MACD
def macd(panel_data):
    panel_data['ema_12'] = panel_data.groupby('Ticker')['Close'].ewm(span=12, adjust=False, min_periods=12).mean().reset_index(drop=True).to_list()
    panel_data['ema_26'] = panel_data.groupby('Ticker')['Close'].ewm(span=26, adjust=False, min_periods=26).mean().reset_index(drop=True).to_list()
    panel_data['macd'] = panel_data['ema_12'] - panel_data['ema_26']
    panel_data['macd_s'] = panel_data.groupby('Ticker')['macd'].ewm(span=9, adjust=False, min_periods=9).mean().reset_index(drop=True).to_list()
    panel_data['macd_h'] = panel_data['macd'] - panel_data['macd_s']
    
    del panel_data['ema_12'],
    del panel_data['ema_26']

    return panel_data


# 3. Percentage Price Oscillator
def ppo(panel_data):
    panel_data['ema_12'] = panel_data.groupby('Ticker')['Close'].ewm(span=12, adjust=False, min_periods=12).mean().reset_index(drop=True).to_list()
    panel_data['ema_26'] = panel_data.groupby('Ticker')['Close'].ewm(span=26, adjust=False, min_periods=26).mean().reset_index(drop=True).to_list()
    panel_data['ppo'] = (panel_data['ema_12'] - panel_data['ema_26'])/panel_data['ema_26']*100
    panel_data['ppo_signal_line'] = panel_data.groupby('Ticker')['ppo'].ewm(span=9, adjust=False, min_periods=9).mean().reset_index(drop=True).to_list()
    panel_data['ppo_histogram'] = panel_data['ppo'] - panel_data['signal_line']
    
    del panel_data['ema_12']
    del panel_data['ema_26']

    return panel_data


# 4. William R
def williamR(panel_data, lookback: int):
    panel_data['highest_high_14'] = panel_data.groupby('Ticker')['High'].rolling(lookback).max().reset_index(drop=True).to_list()
    panel_data['lowest_low_14'] = panel_data.groupby('Ticker')['Low'].rolling(lookback).min().reset_index(drop=True).to_list()
    panel_data[f'{lookback}_day_wr'] = (panel_data['highest_high_14'] - panel_data['Close'])/(panel_data['highest_high_14'] - panel_data['lowest_low_14'])*(-100)
    
    del panel_data['highest_high_14']
    del panel_data['lowest_low_14']
    
    return panel_data


# 5. Chande Momentum Oscillator
def chandeMO(panel_data, lookback:int):
    panel_data['previous_close'] = panel_data.groupby('Ticker')['Close'].shift(1)
    panel_data['delta'] = panel_data.groupby('Ticker')['Close'].diff(1)
    panel_data['higher_close'] = np.where(panel_data['delta']>=0, panel_data['delta'], 0)
    panel_data['lower_close'] = np.where(panel_data['delta']<0, panel_data['delta']*(-1), 0)
    panel_data['higher_close_14'] = panel_data.groupby('Ticker')['higher_close'].rolling(lookback).sum().reset_index(drop=True).to_list()
    panel_data['lower_close_14'] = panel_data.groupby('Ticker')['lower_close'].rolling(lookback).sum().reset_index(drop=True).to_list()
    panel_data[f'chande_mo_{lookback}'] = (panel_data['higher_close_14'] - panel_data['lower_close_14'])/(panel_data['higher_close_14'] + panel_data['lower_close_14'])*100
    
    del panel_data['previous_close']
    del panel_data['delta']
    del panel_data['higher_close']
    del panel_data['lower_close']
    del panel_data['higher_close_14']
    del panel_data['lower_close_14']
    
    return panel_data


# 6. Commodity Channel Index
def cci(panel_data, lookbacks: int):
    panel_data['typical_price'] = np.mean(panel_data[['High', 'Low', 'Close']], axis=1)
    panel_data['typical_price_ma14'] = panel_data.groupby('Ticker')['typical_price'].rolling(lookbacks).mean().reset_index(drop=True).to_list()
    panel_data['typical_price_std14'] = panel_data.groupby('Ticker')['typical_price'].rolling(lookbacks).std().reset_index(drop=True).to_list()
    panel_data[f'cci_{lookbacks}'] = (panel_data['typical_price'] - panel_data['typical_price_ma14'])/(0.015 * panel_data['typical_price_std14'])

    del panel_data['typical_price']
    del panel_data['typical_price_ma14']
    del panel_data['typical_price_std14']

    return panel_data


# Process Volume Group
# 1. On Balance Volume
def obv(panel_data):
    panel_data['previous_close'] = panel_data.groupby('Ticker')['Close'].shift(1).reset_index(drop=True).to_list()
    panel_data['up'] = np.where(panel_data['Close'] > panel_data['previous_close'], 1, 0)
    panel_data['down'] = np.where(panel_data['Close'] < panel_data['previous_close'], -1, 0)
    panel_data['unchanged'] = np.where(panel_data['Close'] == panel_data['previous_close'], 0, 0)
    panel_data['according_vol'] = panel_data['Volume'] * np.sum(panel_data[['up', 'down', 'unchanged']], axis= 1)

    panel_data['OBV'] = panel_data.groupby('Ticker')['according_vol'].cumsum()
    
    del panel_data['previous_close']
    del panel_data['up']
    del panel_data['down']
    del panel_data['unchanged']
    del panel_data['according_vol']
    
    return panel_data


# 2. Money Flow Index
def mfi(panel_data, lookback: int):
    panel_data['typical_price'] = panel_data[['Close', 'High', 'Low']].mean(axis=1)
    panel_data['money_flow'] = panel_data['Volume'] * panel_data['typical_price']
    panel_data['positive_money_flow'] = np.where(panel_data.groupby('Ticker')['typical_price'].diff(1) > 0, panel_data.groupby('Ticker')['typical_price'].shift(1), 0)
    panel_data['negative_money_flow'] = np.where(panel_data.groupby('Ticker')['typical_price'].diff(1) < 0, panel_data.groupby('Ticker')['typical_price'].shift(1), 0)
    panel_data['neutral_money_flow'] = np.where(panel_data.groupby('Ticker')['typical_price'].diff(1) == 0, 0, 0)
    panel_data['positive_money_flow_ma'] = panel_data.groupby('Ticker')['positive_money_flow'].rolling(lookback).mean().reset_index(drop=True).to_list()
    panel_data['negative_money_flow_ma'] = panel_data.groupby('Ticker')['negative_money_flow'].rolling(lookback).mean().reset_index(drop=True).to_list()

    panel_data['money_flow_ratio'] = panel_data['positive_money_flow_ma']/panel_data['negative_money_flow_ma']
    panel_data[f'mfi_{lookback}'] = 100 - 100/(1+panel_data['money_flow_ratio'])
    
    del panel_data['typical_price'] 
    del panel_data['money_flow'] 
    del panel_data['positive_money_flow']
    del panel_data['negative_money_flow']
    del panel_data['neutral_money_flow']
    del panel_data['positive_money_flow_ma'] 
    del panel_data['negative_money_flow_ma']
    del panel_data['money_flow_ratio']

    return panel_data


# 4. Accumulation and Distribution Line
def accumulation_distribution(panel_data):
    for index, row in panel_data.iterrows():
        if row['High'] != row['Low']:
            ac = ((row['Close'] - row['Low']) - (row['High'] - row['Close']))/(row['High'] - row['Low']) * row['Volume']
        else:
            ac = 0
        panel_data.at[index, 'mf_volume'] = ac
    
    panel_data['acc_dist_line'] = panel_data.groupby('Ticker')['mf_volume'].cumsum()
    
    del panel_data['mf_volume']
    
    return panel_data


# Process Volatility Group
# 1. Bollinger Bands
def bbands(panel_data):
    panel_data["ma_10"] = panel_data.groupby('Ticker')['Close'].rolling(10, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["upper_b10"] = panel_data["ma_10"] + panel_data.groupby('Ticker')['Close'].rolling(10, min_periods=1).std().reset_index(drop=True).to_list()
    panel_data["lower_b10"] = panel_data["ma_10"] - panel_data.groupby('Ticker')['Close'].rolling(10, min_periods=1).std().reset_index(drop=True).to_list()

    panel_data["ma_20"] = panel_data.groupby('Ticker')['Close'].rolling(20, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["upper_b20"] = panel_data["ma_20"] + panel_data.groupby('Ticker')['Close'].rolling(20, min_periods=1).std().reset_index(drop=True).to_list()
    panel_data["lower_b20"] = panel_data["ma_20"] - panel_data.groupby('Ticker')['Close'].rolling(20, min_periods=1).std().reset_index(drop=True).to_list()

    panel_data["ma_30"] = panel_data.groupby('Ticker')['Close'].rolling(30, min_periods=1).mean().reset_index(drop=True).to_list()
    panel_data["upper_b30"] = panel_data["ma_30"] + panel_data.groupby('Ticker')['Close'].rolling(30, min_periods=1).std().reset_index(drop=True).to_list()
    panel_data["lower_b30"] = panel_data["ma_30"] - panel_data.groupby('Ticker')['Close'].rolling(30, min_periods=1).std().reset_index(drop=True).to_list()
    
    return panel_data



if __name__ == "__main__":
    print("Hello World")