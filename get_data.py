import pandas as pd
import numpy as np
from src import technical_indicators as ta
from VnFinance import vn_stock_market as vsm


stocks = ['ACB', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR',
         'HDB', 'HPG', 'KDH', 'MBB', 'MSN', 'MWG', 'NVL',
         'PDR', 'PLX', 'POW', 'SAB', 'SSI', 'STB', 'TCB',
         'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VJC', 'VNM',
         'VPB', 'VRE']

for stock in stocks:
    hpg = vsm.get_stock_data(symbol=stock, freq='D')

    lb_rsi = [10, 15, 20, 25]
    for i in lb_rsi:
        hpg = ta.rsi(hpg, i)
        
    lb_natr = [10, 15, 20]
    for i in lb_natr:
        hpg = ta.natr(hpg, i)

    hpg = ta.obv(hpg)
    hpg = ta.accumulation_distribution(hpg)

    lb_wr = [10, 15, 20]
    for i in lb_wr:
        hpg = ta.williamR(hpg, i)

    hpg = ta.triple_ema(hpg)

    lb_roc = [5, 10, 20, 40, 80]
    for i in lb_roc:
        hpg = ta.roc(hpg, i)

    hpg = ta.ppo(hpg)
    hpg = ta.ppo(hpg, fast_ema=9, slow_ema=20, signal_line=9)

    lb_mfi = [10, 14, 20]
    for i in lb_mfi:
        hpg = ta.mfi(hpg, i)

    hpg = ta.macd(hpg)

    hpg = ta.chandeMO(hpg, 14)

    lb_cci = [14, 28]
    for i in lb_cci:
        hpg = ta.cci(hpg, i)

    lb_disparity = [1, 2, 5, 10, 20, 50, 100]
    for i in lb_disparity:
        hpg = ta.disparity_index(hpg, i)

    hpg = ta.bbands(hpg)

    hpg.to_csv(f'cache/{stock}.csv')
    print(f"Downloaded {stock}")