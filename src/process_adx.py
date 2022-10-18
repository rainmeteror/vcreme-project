import pandas as pd
import numpy as np

df = pd.read_csv(r"E:\Tung\Python\VcreamProject\cache\ALL.csv")

df.drop(['Unnamed: 0'], axis = 1, inplace=True)