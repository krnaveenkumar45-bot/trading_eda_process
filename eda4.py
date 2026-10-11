import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv", dtype=str)
df = df.drop_duplicates()                              # remove duplicate rows

# timestamps: Unix seconds/ms, DD/MM/YYYY, and standard format -> one datetime
def fix_time(s):
    s = str(s).strip()
    if s.isdigit():                                    # unix time
        unit = "ms" if len(s) >= 13 else "s"
        return pd.to_datetime(int(s), unit=unit)
    if "/" in s:                                       # DD/MM/YYYY
        return pd.to_datetime(s, dayfirst=True)
    return pd.to_datetime(s)                           # standard format

df["timestamp"] = df["timestamp"].apply(fix_time)

df["symbol"] = df["symbol"].str.upper().str.replace("/", "").str.replace("-", "")
df["side"] = df["side"].str.strip().str.lower()        # buy / sell

# prices and quantities: remove $ and commas, then make them numbers
num_cols = ["price", "quantity", "bid_price_1", "bid_qty_1",
            "ask_price_1", "ask_qty_1"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c].str.replace(r"[$,]", "", regex=True), errors="coerce")

# missing side: guess from price (at ask = buy, at bid = sell)
df.loc[df["side"].isna() & (df["price"] >= df["ask_price_1"]), "side"] = "buy"
df.loc[df["side"].isna() & (df["price"] <= df["bid_price_1"]), "side"] = "sell"

# drop rows that still have missing important values
df = df.dropna(subset=["price", "quantity", "bid_price_1", "bid_qty_1",
                       "ask_price_1", "ask_qty_1", "side"])

# remove bad values
df = df[(df["price"] > 0) & (df["quantity"] > 0)]      # no zero or negative
df = df[df["bid_price_1"] <= df["ask_price_1"]]        # no crossed book

# outlier prices: compare with the order book middle price
mid = (df["bid_price_1"] + df["ask_price_1"]) / 2
gap = (df["price"] / mid - 1).abs()
fix_x100 = (df["price"] / 100 / mid - 1).abs() < 0.02  # price is 100 times too big
df.loc[(gap > 0.02) & fix_x100, "price"] = df["price"] / 100
gap = (df["price"] / mid - 1).abs()
df = df[gap <= 0.02]                                   # drop anything still far off

# sort by time and remove duplicate trade_id
df = df.sort_values("timestamp").drop_duplicates(subset="trade_id")
df.to_csv("trades_clean.csv", index=False)
print("clean rows:", len(df))

