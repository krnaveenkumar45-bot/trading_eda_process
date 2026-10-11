import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv", dtype=str)
# convert numeric columns from text to numbers
num_cols = ["price", "quantity", "bid_price_1", "bid_qty_1",
            "ask_price_1", "ask_qty_1", "bid_price_2", "bid_qty_2",
            "bid_price_3", "bid_qty_3", "ask_price_2", "ask_qty_2",
            "ask_price_3", "ask_qty_3"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c].str.replace(r"[$,]", "", regex=True), errors="coerce")
# step3: find problems
# 1. missing values
print(df.isnull().sum())                               # missing per column

# 2. duplicates
print("duplicate rows:", df.duplicated().sum())
print("duplicate trade_id:", df["trade_id"].duplicated().sum())

# 3. mixed timestamp formats
# replaces every digit with 9 so formats show up as patterns
print(df["timestamp"].str.replace(r"\d", "9", regex=True).value_counts())

# 4. negative or zero values
print("price <= 0:", (df["price"] <= 0).sum())
print("quantity <= 0:", (df["quantity"] <= 0).sum())

# 5. crossed books (best bid higher than best ask)
print("crossed books:", (df["bid_price_1"] > df["ask_price_1"]).sum())