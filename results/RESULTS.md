# Trading Data EDA: Results by Step

Data: `trades_orderbook_STUDENT_dirty.csv` (synthetic BTCUSDT, 2026-10-01, 09:00 to 09:27)

## Step 1: Load and inspect
- Shape: (2035, 18)
- 18 columns: trade_id, timestamp, symbol, side, price, quantity, bid/ask price and qty for levels 1 to 3
- Non-null counts: side 2020, price 2010, quantity 2015, bid_qty_1 2005, ask_price_1 2015

## Step 2: Summarize
Price and quantity (raw data, after converting text to numbers):

| Stat   | price        | quantity |
|--------|--------------|----------|
| min    | -62,183.70   | 0.0000   |
| max    | 6,225,050.00 | 2.7894   |
| mean   | 86,215.82    | 0.0806   |
| median | 62,116.35    | 0.0488   |

The negative and very large prices are the dirty values that step 4 corrects or removes.

Side counts (raw): buy 970, sell 930, BUY 63, Sell 57, missing 15
Symbol counts (raw): BTCUSDT 1974, btcusdt 24, BTC/USDT 21, BTC-USDT 16

## Step 3: Find problems

| Check                       | Result                                                    |
|-----------------------------|-----------------------------------------------------------|
| Missing values              | side 15, price 25, quantity 20, bid_qty_1 30, ask_price_1 20 |
| Duplicate rows              | 35                                                        |
| Duplicate trade_id          | 35                                                        |
| Timestamp formats           | 1917 standard, 78 DD/MM/YYYY, 40 Unix seconds             |
| Price <= 0                  | 6                                                         |
| Quantity <= 0               | 6                                                         |
| Crossed books (bid > ask)   | 10                                                        |

## Step 4: Clean

| Step                          | Rows after | Rows dropped |
|-------------------------------|-----------:|-------------:|
| Start                         | 2035       | -            |
| Remove duplicates             | 2000       | 35           |
| Drop missing required values  | 1905       | 95           |
| Drop zero/negative values     | 1893       | 12           |
| Drop crossed books            | 1883       | 10           |
| Price outliers (x100 fixed, far-off dropped) | 1883 | 0 |
| **Final clean rows**          | **1883**   | **152 total** |

Side after cleaning: buy 963, sell 920. Symbol: all BTCUSDT.
Output: `trades_clean.csv`

## Step 5: Outliers (IQR)
- Q1 = 62,042.65, Q3 = 62,171.60, IQR = 128.95
- Fences: 61,849.23 and 62,365.02
- Outliers found: 0
- Rows after removal: 1883

## Step 6: Features (per trade)
| Feature         | Count | Mean      | Min      | Max       |
|-----------------|------:|----------:|---------:|----------:|
| spread          | 1883  | 0.176     | 0.10     | 0.50      |
| mid_price       | 1883  | 62,109.20 | 61,954.05| 62,253.95 |
| order_imbalance | 1883  | -0.033    | -0.980   | 0.986     |
| volatility_20   | 1863  | 0.000067  | 0.000033 | 0.000095  |
| ma_10           | 1874  | 62,109.38 | 61,961.95| 62,250.31 |
| rsi_14          | 1869  | 51.33     | 7.54     | 94.64     |

Output: `features_tick.csv`

## Step 7: 1-minute candles
- Number of candles: 28 (09:00 to 09:27)
- Total volume: 153.9892
- Total quantity in trades: 153.9892 (matches)
- Total trades across candles: 1883 (all trades counted once)
- Output: `candles_1min.csv`

## Step 8: Visualization
- Price chart: rises from about 61,970 to about 62,240, dips to about 62,150 at the end
- Volume histogram: most minutes between 5 and 6
- Spread distribution: most trades at 0.10
- Buy vs sell: 963 buy, 920 sell
- Correlation heatmap: most values near 0; return and rsi_14 = 0.27; volatility_20 and ma_10 = -0.14
- Output: `step8_charts.png`, `step8_heatmap.png`

## Step 9: Model preparation
- Features: return, volatility_5, ma_gap, volume, trade_count (per 1-minute candle)
- Target: price up in 5 minutes (1 = up, 0 = down)
- Rows: 16 (28 candles minus 7 at start and 5 at end)
- Train: 11 rows (09:07 to 09:17), 81.8% up
- Test: 5 rows (09:18 to 09:22), 40% up
- Features scaled using training statistics only
- Output: `model_data_clean.csv`, `train_scaled.csv`, `test_scaled.csv`

## Notes
- The sample covers only 28 minutes, so the model results are a demonstration of the process, not a usable trading model.
- The training set is heavily imbalanced (82% up), so a model that always predicts "up" would look good on training but poor on test.
