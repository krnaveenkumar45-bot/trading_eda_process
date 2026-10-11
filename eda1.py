import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# step1: load the data (read everything as text first)
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv", dtype=str)
print("shape:", df.shape)
print(df.head())
print(df.info())