# step2: summarize
# convert price and quantity to numbers first, so min/max/mean/median work
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv", dtype=str)
df["price"] = pd.to_numeric(df["price"].str.replace(r"[$,]", "", regex=True), errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"].str.replace(r"[$,]", "", regex=True), errors="coerce")

print(df.describe())                                   # count, mean, std, min, max, quartiles
print(df["side"].value_counts(dropna=False))           # buy / sell / BUY / Sell / missing
print(df["symbol"].value_counts(dropna=False))         # BTCUSDT / btcusdt / BTC/USDT / BTC-USDT

# min, max, mean, median for price and quantity
print(df[["price", "quantity"]].agg(["min", "max", "mean", "median"]))