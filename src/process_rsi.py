import pandas as pd
import numpy as np

df = pd.read_csv(r"E:\Tung\Python\VcreamProject\cache\ALL.csv")

df.drop(['Unnamed: 0'], axis = 1, inplace=True)

df['delta'] = delta = df.groupby('Ticker')['Close'].diff()
df['up'] = df['delta'].clip(lower=0)
df['down'] = -1*df['delta'].clip(upper=0)

df['ema_up'] = df.groupby('Ticker')['up'].ewm(com=13, adjust=False).mean().reset_index(drop=True).to_list()
df['ema_down'] = df.groupby('Ticker')['down'].ewm(com=13, adjust=False).mean().reset_index(drop=True).to_list()

df['rs'] = df['ema_up']/df['ema_down']
df['rsi'] = 100 - (100/(1+df['rs']))

print(df)

