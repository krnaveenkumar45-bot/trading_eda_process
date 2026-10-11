import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# step6: feature engineering
# load the cleaned file (prices are already numbers, timestamps already parsed)
df = pd.read_csv("trades_clean.csv", parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# order book features (from level 1 of the book)
df["spread"] = df["ask_price_1"] - df["bid_price_1"]             # gap between sell and buy price
df["mid_price"] = (df["ask_price_1"] + df["bid_price_1"]) / 2    # middle of the book
df["order_imbalance"] = (df["bid_qty_1"] - df["ask_qty_1"]) / (df["bid_qty_1"] + df["ask_qty_1"])

# return: % change from the previous trade
df["return"] = df["price"].pct_change()

# rolling volatility: how much the last 20 returns move around
df["volatility_20"] = df["return"].rolling(20).std()

# moving averages: average price of the last 10 and 30 trades
df["ma_10"] = df["price"].rolling(10).mean()
df["ma_30"] = df["price"].rolling(30).mean()

# RSI (optional): compares recent gains with recent losses, 0 to 100
change = df["price"].diff()
gain = change.clip(lower=0).rolling(14).mean()
loss = (-change.clip(upper=0)).rolling(14).mean()
df["rsi_14"] = 100 - 100 / (1 + gain / loss)

df.to_csv("features_tick.csv", index=False)
print(df[["spread", "mid_price", "order_imbalance", "return",
          "volatility_20", "ma_10", "rsi_14"]].describe())