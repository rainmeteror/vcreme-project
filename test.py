from VnFinance import vn_stock_market as vnf
from src import technical_indicators as ta
import requests
import pandas as pd
import numpy as np


df = vnf.get_bs_data('BID')

print(df.columns)