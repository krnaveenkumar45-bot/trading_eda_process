import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv", dtype=str)
# step5: outliers using IQR on the cleaned price
df["price"] = pd.to_numeric(df["price"].str.replace(r"[$,]", "", regex=True), errors="coerce")
df = pd.read_csv("trades_clean.csv")
q1 = df["price"].quantile(0.25)
q3 = df["price"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[(df["price"] < lower) | (df["price"] > upper)]
print("Q1:", q1, "Q3:", q3, "IQR:", iqr)
print("fences:", lower, upper)
print("outliers found:", len(outliers))
print(outliers[["trade_id", "timestamp", "price"]])

# remove them
df = df[(df["price"] >= lower) & (df["price"] <= upper)]
print("rows after outlier removal:", len(df))