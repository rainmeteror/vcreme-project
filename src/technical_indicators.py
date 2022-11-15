import pandas as pd
import numpy as np 

pd.set_option('mode.chained_assignment', None)

# Process Trend Group

# 1. Moving Average
def moving_average(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate moving average of stock based on Close price
    
    panel_data: pd.DataFrame()
        Panel Data of a stock.
    
    lookback: int
        Parameter for moving average
        
    """
    panel_data[f"ma_{lookback}"] = panel_data.groupby('Ticker')['Close'].rolling(lookback, min_periods=1).mean().reset_index(drop=True).to_list()
    
    return panel_data


# 2. Triple EMA
def triple_ema(panel_data) -> pd.DataFrame():
    """ Calculate triple exponential moving average
    
    panel_data: pd.DataFrame()
        Panel Data of a stock.
    
    """
    panel_data['ema_1'] = panel_data.groupby('Ticker')['Close'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()
    panel_data['ema_2'] = panel_data.groupby('Ticker')['ema_1'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()
    panel_data['ema_3'] = panel_data.groupby('Ticker')['ema_2'].ewm(span=30, adjust=False).mean().reset_index(drop=True).to_list()

    panel_data['triple_ema'] = 3*panel_data['ema_1'] - 3*panel_data['ema_2'] + panel_data['ema_3']
    
    del panel_data['ema_1']
    del panel_data['ema_2']
    del panel_data['ema_3']
    
    return panel_data


# 3. Rate of Change ROC
def roc(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate rate of change of a stock based on closed price
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    lookback: int
        Parameter for rate of change
    
    """
    panel_data[f'roc_{lookback}'] = panel_data.groupby('Ticker')['Close'].diff(lookback)/panel_data.groupby('Ticker')['Close'].shift(lookback)

    return panel_data
    

# 4. Normalized Average True Range
def natr(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate normalized average true range
    
    panel_data: pd.DataFrame()
        Panel data of a stock
        
    lookback: int
        Parameter for normalized average true range
        
    """
    panel_data['previous_close'] = panel_data.groupby('Ticker')['Close'].shift(1)
    panel_data['high-low'] = panel_data['High'] - panel_data['Low']
    panel_data['high-pc'] = np.abs(panel_data['High'] - panel_data['previous_close'])
    panel_data['low-pc'] = np.abs(panel_data['Low'] - panel_data['previous_close'])
    panel_data['true_range'] = np.max(panel_data[['high-low', 'high-pc', 'low-pc']], axis=1)

    panel_data[f'atr_{lookback}'] = panel_data.groupby('Ticker')['true_range'].rolling(lookback).mean().reset_index(drop=True).to_list()
    panel_data[f'natr_{lookback}'] = panel_data[f'atr_{lookback}']/panel_data['Close']*100

    
    del panel_data['previous_close']
    del panel_data['high-low']
    del panel_data['high-pc']
    del panel_data['low-pc']
    del panel_data['true_range']
    del panel_data[f'atr_{lookback}']


    return panel_data


# 5. Disparity Index
def disparity_index(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate disparity index. It is the difference between close price and its moving average
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    lookback: int
        Parameter of disparity index
        
    """
    
    panel_data['moving_average_14'] = panel_data.groupby('Ticker')['Close'].rolling(lookback).mean().reset_index(drop=True).to_list()
    panel_data[f'disparity_index_{lookback}'] = (panel_data['Close'] - panel_data['moving_average_14'])/(panel_data['moving_average_14'])*100
    
    del panel_data['moving_average_14']
    
    return panel_data


# 6. Exponential Moving Average
def ema(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate exponential moving average
    
    panel_data: pd.DataFrame()
        Panel data of a stock
        
    lookback: int
        Parameter of exponential moving average
        
    """
    panel_data[f'ema_{lookback}'] = panel_data.groupby('Ticker')['Close'].ewm(span=lookback, adjust=False).mean().reset_index(drop=True).to_list()
    
    return panel_data

# Process Momentum Group
# 1. RSI
def rsi(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate RSI - Relative strength index
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    lookback: int
        Parameter of RSI
        
    """
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
def macd(panel_data) -> pd.DataFrame():
    """ Calculate MACD - Moving average convergence and divergence
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    """
    panel_data['ema_12'] = panel_data.groupby('Ticker')['Close'].ewm(span=12, adjust=False, min_periods=12).mean().reset_index(drop=True).to_list()
    panel_data['ema_26'] = panel_data.groupby('Ticker')['Close'].ewm(span=26, adjust=False, min_periods=26).mean().reset_index(drop=True).to_list()
    panel_data['macd'] = panel_data['ema_12'] - panel_data['ema_26']
    panel_data['macd_s'] = panel_data.groupby('Ticker')['macd'].ewm(span=9, adjust=False, min_periods=9).mean().reset_index(drop=True).to_list()
    panel_data['macd_h'] = panel_data['macd'] - panel_data['macd_s']
    
    del panel_data['ema_12'],
    del panel_data['ema_26']

    return panel_data


# 3. Percentage Price Oscillator
def ppo(panel_data, fast_ema = 12, slow_ema = 26, signal_line = 9) -> pd.DataFrame():
    """ Calculate percentage price oscilator
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    fast_ema: int
        Fast exponential moving average of close price
        Defaul value: 12
    
    slow_ema: int
        Slow exponential moving average of close price
        Defaul value: 12
    
    signal_line: int
        Signal line of difference between Fast and Slow exponential moving average
        Defaul value: 12
        
    """
    panel_data['ema_12'] = panel_data.groupby('Ticker')['Close'].ewm(span=fast_ema, adjust=False, min_periods=fast_ema).mean().reset_index(drop=True).to_list()
    panel_data['ema_26'] = panel_data.groupby('Ticker')['Close'].ewm(span=slow_ema, adjust=False, min_periods=slow_ema).mean().reset_index(drop=True).to_list()
    panel_data[f'ppo_{fast_ema}_{slow_ema}'] = (panel_data['ema_12'] - panel_data['ema_26'])/panel_data['ema_26']*100
    panel_data[f'ppo_signal_line_{signal_line}'] = panel_data.groupby('Ticker')[f'ppo_{fast_ema}_{slow_ema}'].ewm(span=signal_line, adjust=False, min_periods=signal_line).mean().reset_index(drop=True).to_list()
    panel_data[f'ppo_histogram_{fast_ema}_{slow_ema}_{signal_line}'] = panel_data[f'ppo_{fast_ema}_{slow_ema}'] - panel_data[f'ppo_signal_line_{signal_line}']
    
    del panel_data['ema_12']
    del panel_data['ema_26']

    return panel_data


# 4. William R
def williamR(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate William R
    
    panel_data: pd.DataFrame()
        Panel data of a stock
        
    lookback: int
        Parameter of William R
        
    """
    panel_data['highest_high_14'] = panel_data.groupby('Ticker')['High'].rolling(lookback).max().reset_index(drop=True).to_list()
    panel_data['lowest_low_14'] = panel_data.groupby('Ticker')['Low'].rolling(lookback).min().reset_index(drop=True).to_list()
    panel_data[f'{lookback}_day_wr'] = (panel_data['highest_high_14'] - panel_data['Close'])/(panel_data['highest_high_14'] - panel_data['lowest_low_14'])*(-100)
    
    del panel_data['highest_high_14']
    del panel_data['lowest_low_14']
    
    return panel_data


# 5. Chande Momentum Oscillator
def chandeMO(panel_data, lookback:int) -> pd.DataFrame():
    """ Calculate Chande Momentum Oscillator
    
    panel_data: pd.DataFrame()
        Panel data of a stock
        
    lookback: int
        Parameter of change momentum oscillator
        
    """
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
def cci(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate CCI - Commodity channel index
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    lookback: int
        Parameter of CCI
    """
    panel_data['typical_price'] = np.mean(panel_data[['High', 'Low', 'Close']], axis=1)
    panel_data['typical_price_ma14'] = panel_data.groupby('Ticker')['typical_price'].rolling(lookback).mean().reset_index(drop=True).to_list()
    panel_data['typical_price_std14'] = panel_data.groupby('Ticker')['typical_price'].rolling(lookback).std().reset_index(drop=True).to_list()
    panel_data[f'cci_{lookback}'] = (panel_data['typical_price'] - panel_data['typical_price_ma14'])/(0.015 * panel_data['typical_price_std14'])

    del panel_data['typical_price']
    del panel_data['typical_price_ma14']
    del panel_data['typical_price_std14']

    return panel_data


# Process Volume Group
# 1. On Balance Volume
def obv(panel_data) -> pd.DataFrame():
    """ Calculate on balance volume
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    """
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
def mfi(panel_data, lookback: int) -> pd.DataFrame():
    """ Calculate money flow index
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    
    lookback: int
        Parameter of MFI
    """
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
def accumulation_distribution(panel_data) -> pd.DataFrame():
    """ calculate accumulation and distribution of a stock based on prices
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    """
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
def bbands(panel_data) -> pd.DataFrame():
    """ Calculate Bollinger bands
    
    panel_data: pd.DataFrame()
        Panel data of a stock
    """
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