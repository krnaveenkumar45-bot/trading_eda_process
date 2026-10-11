import pandas as pd

# load the 1-minute candles from step 7
candles = pd.read_csv("candles_1min.csv", parse_dates=["timestamp"])
candles = candles.sort_values("timestamp").reset_index(drop=True)

# 1. features (each one uses only past and current candles)
candles["return"] = candles["close"].pct_change()
candles["volatility_5"] = candles["return"].rolling(5).std()
candles["ma_3"] = candles["close"].rolling(3).mean()
candles["ma_8"] = candles["close"].rolling(8).mean()
candles["ma_gap"] = candles["ma_3"] / candles["ma_8"] - 1

feature_cols = ["return", "volatility_5", "ma_gap", "volume", "trade_count"]

# 2. target: will the price be higher 5 minutes from now? (1 = up, 0 = down)
#    shift(-5) looks 5 candles ahead, so this is the only column that uses future data
future_close = candles["close"].shift(-5)
candles["target_up_5m"] = (future_close > candles["close"]).astype(float)
candles.loc[future_close.isna(), "target_up_5m"] = float("nan")   # last 5 candles have no answer

# drop rows that are missing a feature or the target (start and end of the data)
data = candles.dropna(subset=feature_cols + ["target_up_5m"]).reset_index(drop=True)
data.to_csv("model_data_clean.csv", index=False)

# 3. split by time, 70% train / 30% test (no shuffling)
split = int(len(data) * 0.70)
train = data.iloc[:split].copy()
test = data.iloc[split:].copy()
print("rows:", len(data), "| train:", len(train), "| test:", len(test))
print("train period:", train["timestamp"].min(), "->", train["timestamp"].max())
print("test period: ", test["timestamp"].min(), "->", test["timestamp"].max())

# 4. scale features using TRAINING numbers only (no information from the test period)
mu = train[feature_cols].mean()
sd = train[feature_cols].std()
train[feature_cols] = (train[feature_cols] - mu) / sd
test[feature_cols] = (test[feature_cols] - mu) / sd

# 5. save the prepared files
train.to_csv("train_scaled.csv", index=False)
test.to_csv("test_scaled.csv", index=False)

# class balance: how often the price went up
print("share up in train:", round(train["target_up_5m"].mean(), 3))
print("share up in test: ", round(test["target_up_5m"].mean(), 3))