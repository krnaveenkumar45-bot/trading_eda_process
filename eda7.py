import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# step7: resample trades into 1-minute OHLCV candles
df = pd.read_csv("trades_clean.csv", parse_dates=["timestamp"])
df = df.sort_values("timestamp").set_index("timestamp")

# open = first price, high = highest, low = lowest, close = last price
candles = df["price"].resample("1min").ohlc()

# volume = total quantity traded in that minute
candles["volume"] = df["quantity"].resample("1min").sum()

# how many trades happened in that minute
candles["trade_count"] = df["price"].resample("1min").count()

# minutes with no trades: keep the last close, set volume to 0
candles["close"] = candles["close"].ffill()
candles["open"] = candles["open"].fillna(candles["close"])
candles["high"] = candles["high"].fillna(candles["close"])
candles["low"] = candles["low"].fillna(candles["close"])
candles["volume"] = candles["volume"].fillna(0)
candles["trade_count"] = candles["trade_count"].fillna(0)

print(candles.head())
print("number of candles:", len(candles))
print("total volume:", round(candles["volume"].sum(), 4))
print("total quantity in trades:", round(df["quantity"].sum(), 4))

candles.to_csv("candles_1min.csv")