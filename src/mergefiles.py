import pandas as pd
import numpy as np


list_path = [
    r"E:\Tung\Python\VcreamProject\cache\CafeF.HNX.Upto18.10.2022.csv",
    r"E:\Tung\Python\VcreamProject\cache\CafeF.HSX.Upto18.10.2022.csv",
    r"E:\Tung\Python\VcreamProject\cache\CafeF.UPCOM.Upto18.10.2022.csv"
]

df = pd.concat(pd.read_csv(l) for l in list_path)

df.columns = ["Ticker", "Date", "Open", "High" ,"Low", "Close", "Volume"]
df['Date'] = pd.to_datetime(df['Date'], format="%Y%m%d")

df.sort_values(['Ticker', 'Date'], inplace=True)
df.to_csv(r"E:\Tung\Python\VcreamProject\cache\ALL.csv")
print("Merged all files into all.csv file")