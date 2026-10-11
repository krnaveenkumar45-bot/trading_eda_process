import pandas as pd
import matplotlib.pyplot as plt

# load the files from earlier steps
candles = pd.read_csv("candles_1min.csv", parse_dates=["timestamp"])
trades = pd.read_csv("features_tick.csv")

# 1. price line chart + 2. volume histogram + 3. spread distribution + 4. buy vs sell
fig, ax = plt.subplots(2, 2, figsize=(12, 9))

ax[0, 0].plot(candles["timestamp"], candles["close"])
ax[0, 0].set_title("Price (1-min close)")
ax[0, 0].tick_params(axis="x", rotation=45)

ax[0, 1].hist(candles["volume"], bins=20, color="tab:blue")
ax[0, 1].set_title("Volume per minute")

ax[1, 0].hist(trades["spread"], bins=20, color="tab:green")
ax[1, 0].set_title("Spread distribution")

counts = trades["side"].value_counts()
ax[1, 1].bar(counts.index, counts.values, color=["tab:green", "tab:red"])
ax[1, 1].set_title("Buy vs sell counts")

fig.tight_layout()
fig.savefig("step8_charts.png")

# 5. correlation heatmap of the features
features = ["spread", "order_imbalance", "return", "volatility_20", "ma_10", "rsi_14"]
corr = trades[features].corr()

plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(features)), features, rotation=45, ha="right")
plt.yticks(range(len(features)), features)
for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
plt.title("Feature correlation heatmap")
plt.tight_layout()
plt.savefig("step8_heatmap.png")

plt.show()